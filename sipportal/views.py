from django.shortcuts import redirect, render
from util import func
def index(request):
    print(func.sendotp("sqlmy321@gmail.com"))
    return render(request,'index.html')
# Added by Laavesh
def about(request):
    return render(request, 'about_us.html')