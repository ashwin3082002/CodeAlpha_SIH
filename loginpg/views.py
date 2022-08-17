from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def student(request):
    if request.method=='POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            if request.user.is_staff or request.user.is_superuser:
                messages.error(request, "Login not permitted")
                logout(request)
            return redirect('/dashboard/student')
        else:
            messages.error(request, "Incorrect Credentials")
    return render(request, 'login-student.html')

def institution(request):
    if request.method=='POST':
            username = request.POST.get('name')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                if request.user.is_staff and not request.user.is_superuser:
                    return redirect('/dashboard/institution')
                else:
                    messages.error(request, "Login not permitted")
                    logout(request)
            else:
                messages.error(request, "Incorrect Credentials")
    return render(request, 'login-institution.html')

def admin(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            if request.user.is_superuser:
                return redirect('/dashboard/admin')
            else:
                messages.error(request, "Login not permitted")
                logout(request)
        else:
            messages.error(request, "Incorrect Credentials")
    return render(request, 'login-admin.html')

def pass_reset_otp(request):
    return render(request,'pass_reset_otp.html')

def resetpassword(request):
    return render(request,'reset-password.html')