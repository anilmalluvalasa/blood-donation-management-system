from django.shortcuts import render,HttpResponse,redirect
from .models import Donar_details
from .models import OTP
import random
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from datetime import timedelta
from django.contrib.auth.hashers import check_password


# Create your views here.
def blood(req):
    return render(req,'HomePage.html')
def regdonar(req):
    if req.method == 'POST':
        did = int(req.POST.get('did'))
        dname = req.POST.get('dname')
        gender = req.POST.get('gender')
        age = int(req.POST.get('age'))
        phno = req.POST.get('phno')
        email = req.POST.get('email')
        bg = req.POST.get('bg')
        state = req.POST.get('state')
        city = req.POST.get('city')

        #  Hash password
        pwd = make_password(req.POST.get('pwd'))

        s = Donar_details(
            did=did, dname=dname, gender=gender,
            age=age, phno=phno, email=email,
            bloodgroup=bg, state=state,
            city=city, password=pwd
        )
        s.save()

        return render(req, 'Registrationpage.html', {'msg': "Registration Successful"})
    else:
        return render(req, 'Registrationpage.html')




def dlogin(req):
    if req.method == 'POST':
        uname = req.POST.get('uname').strip()
        pwd = req.POST.get('pwd').strip()

        # Check username exists
        if Donar_details.objects.filter(dname=uname).exists():
            user = Donar_details.objects.get(dname=uname)

            # Check password properly (hashed)
            if check_password(pwd, user.password):

                if not user.email:
                    return render(req, 'loginpage.html', {'msg1': 'Email not found'})

                otp_obj, created = OTP.objects.get_or_create(user=user)
                otp = otp_obj.generate_otp()

                # SEND EMAIL
                send_mail(
                    'Your OTP Code',
                    f'Your OTP is {otp}',
                    'yourgmail@gmail.com',
                    [user.email],
                )

                req.session['donar_id'] = user.did
                return redirect('verify_otp')

            else:
                return render(req, 'loginpage.html', {'msg1': 'Wrong Password'})

        else:
            return render(req, 'loginpage.html', {'msg1': 'Invalid Username'})

    return render(req, 'loginpage.html')

def verify_otp(req):
    if req.method == 'POST':
        entered_otp = req.POST.get('otp')
        user_id = req.session.get('donar_id')

        user = Donar_details.objects.get(did=user_id)
        otp_obj = OTP.objects.get(user=user)

        if otp_obj.created_at < timezone.now() - timedelta(minutes=5):
            return render(req, 'verify_otp.html', {'msg': 'OTP Expired'})

        if otp_obj.otp_code == entered_otp:
            otp_obj.delete()
            return render(req, 'Loginsuccesspage.html', {'msg': user})
        else:
            return render(req, 'otppage.html', {'msg': 'Invalid OTP'})

    return render(req, 'otppage.html')



def donarupdate(req):
    if req.method=='POST':
        did = req.POST.get('did')
        # state = req.POST.get('state')
        # city = req.POST.get('city')
        # phno = int(req.POST.get('phno'))

        bt = req.POST.get('btn')
        if bt=='Update':
            state = req.POST.get('state')
            city = req.POST.get('city')
            phno = int(req.POST.get('phno'))
            res = Donar_details.objects.get(did=did)
            res.state = state
            res.city = city
            res.phno = phno
            res.save()
            return render(req,'Loginsuccesspage.html',{'u':"Details Updated",'msg':res})
        else:
            return render(req,'HomePage.html')
    else:
        return render(req,'Loginsuccesspage.html')



def Donarsearch(req):
    if req.method == 'POST':
        bg = req.POST.get('bgroup')
        if Donar_details.objects.filter(bloodgroup=bg).exists():
           donors = Donar_details.objects.filter(bloodgroup=bg)
           available_donors = []
           hidden_donors = []
           for d in donors:
                if d.last_donation_date:
                    next_available_date = d.last_donation_date + timedelta(days=90)

                    if timezone.now().date() >= next_available_date:
                        d.availability = "Available"
                        d.save()
                        available_donors.append(d)
                    else:
                        # calculate remaining days
                        remaining_days = (next_available_date - timezone.now().date()).days
                        d.remaining_days = remaining_days
                        hidden_donors.append(d)
                else:
                    available_donors.append(d)
           return render(req, 'DonarSearchpage.html', {
                'res1': available_donors,'hidden': hidden_donors })
        return render(req,'DonarSearchpage.html',{'msg':"No Data Found"})


    else:
        return render(req, 'DonarSearchpage.html')

def donate_blood(req):
    if req.method == 'POST':
        did = req.POST.get('did')

        donor = Donar_details.objects.get(did=did)

        donor.last_donation_date = timezone.now().date()
        donor.availability = "Not Available"
        donor.save()

    return redirect('searchdonar1')

def userrequest(req):
    if req.method=='POST':
        did = int(req.POST.get('did'))
        if Donar_details.objects.filter(did=did).exists():
            res = Donar_details.objects.get(did=did)
            return render(req,'contact.html',{'res':res})
    else:
        return render(req,'searchdonar.html')