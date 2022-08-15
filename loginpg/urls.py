from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('student',views.student),
    path('institution',views.institution),
    path('admin',views.admin),
    path('passwordresetotp',views.pass_reset_otp),
    path('resetpassword',views.resetpassword),
]