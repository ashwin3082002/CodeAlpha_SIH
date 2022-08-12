from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/student',views.student),
    path('login/institution',views.institution),
    path('login/admin',views.admin)
]