from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # admin
    path('admin',views.admin),
    path('admin/search', views.admin_search),
    path('admin/edit', views.admin_edit),
    path('admin/createapi',views.create_api),
    path('admin/revokapi',views.revok_api),
    # insti
    path('institution', views.institution),
    path('institution/search', views.institution_search),
    path('institution/edit', views.institution_edit),
    path('institution/enroll', views.institution_enroll_student),
    path('institution/remove', views.institution_removestudent),
    path('institution/addcourse', views.institution_addcourse),
    path('institution/addcourse/bulk', views.institution_addcourse_bulk),
    # student
    path('student', views.student),
    path('student/getdocument', views.student_get_docu),
]