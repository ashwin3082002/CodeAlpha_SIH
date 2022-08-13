from django.shortcuts import redirect, render

def index(request):
    return render(request,'index.html')

# Added by Laavesh
def about(request):
    return render(request, 'about_us.html')