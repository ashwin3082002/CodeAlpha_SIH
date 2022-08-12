from django.shortcuts import render

# Create your views here.

def student(request):
    return render(request,'login-student.html')

def institution(request):
    return render(request, 'login-institution.html')

def admin(request):
    return render(request, 'login-admin.html')