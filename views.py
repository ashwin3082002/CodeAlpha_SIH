#Added Manually - Ashwin
import random
from studentportal import mysql_commands
from unicodedata import name
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail

def otp_gen(to_mail):
    otp = random.randrange(1111,9999)
    subject = "SIP Account Creation Requested!!"
    mail_message = f"""
Your Otp to create account in the sip portal is: {otp} 

OTP Valid for only 10 Min

Regards,
Admin"""
    send_mail(subject, mail_message, 'student.profile.sih@gmail.com', [to_mail])
    return otp

def index(request):
    return render(request,'index.html')

def student_login(request):
    if request.method == "POST":    
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
    return render(request, 'student_login.html')

def institution_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/institute_dashboard')
        else:
            messages.error(request, "Incorrect Credentials")

    return render(request, "institution_login.html")

def student_create(request):
    name = False
    otp = False    
    if request.method == "POST":
        person_email = ['ashwin3082002@gmail.com']
        name = request.POST.get('name')
        if name:
            email = request.POST.get('email')
            person_email.append(email) 
            otp_gen(email)
        otp = request.POST.get('otp')
        if otp:
            reference_num = random.randrange(1111111111,9999999999)
            subject = "SIP Account Successfully Created!!!"
            mail_message = f"""
Hello {name},
Your profile was succesfully created. 
Your Reference Number: {reference_num}

Your Login will not work until your institution verify you, So kindly visit your institution and verify you documents to get login credentials.
For any queries contact: 044 25256565    

Regards,
Admin"""
            send_mail(subject, mail_message,'student.profile.sih@gmail.com', person_email )
            messages.success(request,"Your Account was created successfully, please read the instruction sent through mail.")
            return HttpResponseRedirect("/student_login")

    return render(request, "student_create.html", {'name': name,'otp':otp})

def institution_create(request):
    name = False
    if request.method == "POST":
        name = request.POST.get('spoc_name')
        insti = request.POST.get('name')
        print(insti, name)

    return render(request, 'institution_create.html', {'name': name })

def insti_dash(request):
    if request.user.is_authenticated:
        return render(request, 'insti_dash.html')
    else:
        return redirect('/institution_login')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('/institution_login')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if mysql_commands.insert_vaules(name,email,message):
            messages.success(request, "Form Submitted Successfully")
    return render(request, 'contact_us.html')