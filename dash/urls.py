from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin',views.admin),
    path('student', views.student),
    path('institution', views.institution),
    path('admin/search', views.admin_search),
    path('admin/edit', views.admin_edit),
]