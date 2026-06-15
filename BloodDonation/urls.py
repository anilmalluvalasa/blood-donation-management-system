"""
URL configuration for BloodDonation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from Donation import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.blood,name='blood'),
    path('dreg/',views.regdonar,name='dreg'),
    path('dlogin/',views.dlogin,name='dlogin'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('donarupdate/',views.donarupdate,name='donarupdate'),
    path('checkdonar/',views.Donarsearch,name='searchdonar1'),
    path('donate-blood/', views.donate_blood, name='donate_blood'),
    path('contact/', views.userrequest, name='request'),
]
