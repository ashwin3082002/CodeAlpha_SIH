from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from sip_db.models import student_detail, institution_detail
from util import func
from django.contrib.auth.models import User

# Create your views here.

def student(request):
    if request.method=='POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            request.session['sid'] = username
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
    request.session['directaccess']=False
    if request.method=="POST":
        if "sendotp" in request.POST:
            common_id = request.POST.get('id')
            res = func.check_id(common_id)
            
            if res == 's':
                request.session['uin'] = common_id
                search_details = student_detail.objects.filter(sid = common_id).values()
                
                if search_details:
                    user_emailid = search_details[0]["email"]
                    user_mobile = search_details[0]["mobile"]
                    otp = func.sendotp(user_emailid, user_mobile)
                    request.session['otp']=otp
                    return render(request, 'pass_reset_otp.html', {'id' : common_id, 'disable':"disabled"})
                else:
                    messages.error(request,'ID not valid.')
                    
            elif res == 'i':
                request.session['uin'] = common_id
                search_details = institution_detail.objects.filter(id = common_id).values()
                
                if search_details:
                    user_emailid = search_details[0]["email"]
                    user_mobile = search_details[0]["mobile"]
                    otp = func.sendotp(user_emailid,user_mobile)
                    request.session['otp']=otp
                    return render(request, 'pass_reset_otp.html', {'id' : common_id, 'disable':"disabled"})
                else:
                    messages.error(request,'ID not valid.')
            else:
                messages.error(request,'ID not valid.')
                return render(request,'pass_reset_otp.html')

        elif 'submit' in request.POST:
            u_otp = request.POST.get('u_otp')
            try:
                if int(u_otp) == int(request.session['otp']):
                    request.session['directaccess']=True
                    return redirect("/login/resetpassword")
                else:
                    messages.error(request, "Wrong OTP")
            except:
                messages.error(request,"Wrong OTP!")

    return render(request,'pass_reset_otp.html')

def resetpassword(request):
    if request.session.get('directaccess')==False or request.session.get('directaccess')==None :
        return redirect("/login/passwordresetotp")
    elif request.session.get('directaccess')==True:
        if request.method == "POST":
            npass = request.POST.get('password')
            cpass = request.POST.get('confirm-password')
            print(npass, cpass)
            if npass == cpass:
                uin = request.session['uin']
                u = User.objects.get(username=uin)
                u.set_password(cpass)
                u.save()
                messages.success(request,"Password Changed")
                return redirect("/")
            else:
                messages.error(request, "Confirm Password Should be same as new password")
                return render(request,'reset-password.html')
        else:
            return render(request,'reset-password.html')