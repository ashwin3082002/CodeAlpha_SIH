from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def student(request):
    return render(request,'login-student.html')

def institution(request):
    return render(request, 'login-institution.html')

def admin(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            request.session['username']=username
            return redirect('/dashboard/admin')
        else:
            messages.error(request, "Incorrect Credentials")
    if request.session.get('username')!=None:
        return redirect('/dashboard/admin') 
    return render(request, 'login-admin.html')

def pass_reset_otp(request):
    return render(request,'pass_reset_otp.html')

def resetpassword(request):
    return render(request,'reset-password.html')