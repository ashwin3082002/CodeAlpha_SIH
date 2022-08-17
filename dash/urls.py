from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin',views.admin),
    path('student', views.student),
    path('insti', views.institution)
]