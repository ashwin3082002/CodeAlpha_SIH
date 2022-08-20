from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request, 'about_us.html')
def terms(request):
    return render(request, 'terms.html')
def privacy(request):
    return render(request, 'privacy.html')
def contact(request):
    return render(request,'contact.html')
def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('/')