from django.shortcuts import render, redirect

# Create your views here.
def admin(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard_admin.html')
    else:
        return redirect('/login/admin')