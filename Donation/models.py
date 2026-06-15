from django.db import models
import random
from django.utils import timezone

# Create your models here.





#My project Code (modifications)

class Donar_details(models.Model):
    did = models.IntegerField(primary_key=True)
    dname = models.CharField(max_length=20)
    gender = models.CharField(max_length=5)
    age = models.IntegerField()
    phno = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    bloodgroup = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    availability = models.CharField(max_length=15, default="Available")
    last_donation_date = models.DateField(null=True, blank=True)

def __str__(self):
        return self.dname
class OTP(models.Model):
    user = models.ForeignKey(Donar_details, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.created_at = timezone.now()
        self.save()
        return self.otp_code

