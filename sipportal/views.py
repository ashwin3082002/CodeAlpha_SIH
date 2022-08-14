from django.shortcuts import redirect, render
from util import func
def index(request):
    return render(request,'index.html')
# Added by Laavesh
def about(request):
    return render(request, 'about_us.html')
def terms(request):
    return render(request, 'terms.html')
def privacy(request):
    return render(request, 'privacy.html')