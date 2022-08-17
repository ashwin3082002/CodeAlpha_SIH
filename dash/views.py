from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
def admin(request):
    if request.user.is_authenticated:
        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam=user.get_full_name()
        return render(request, 'dashboard_admin.html',{'username':uname, 'name':nam, 'email':user_email})
    else:
        return redirect('/login/admin')