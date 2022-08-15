from django.shortcuts import render

# Create your views here.

def student(request):
    return render(request,'login-student.html')

def institution(request):
    return render(request, 'login-institution.html')

def admin(request):
    return render(request, 'login-admin.html')

def pass_reset_otp(request):
    return render(request,'pass_reset_otp.html')

def resetpassword(request):
    return render(request,'reset-password.html')