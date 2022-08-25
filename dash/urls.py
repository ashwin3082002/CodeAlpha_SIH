from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # admin
    path('admin',views.admin),
    path('admin/bulk', views.admin_bulk),
    path('admin/search', views.admin_search),
    path('admin/edit', views.admin_edit),
    path('admin/createapi',views.create_api),
    path('admin/revokapi',views.revok_api),
    # insti
    path('institution', views.institution),
    path('institution/create/bulk', views.institution_createbulk),
    path('institution/search', views.institution_search),
    path('institution/edit', views.institution_edit),
    path('institution/enroll', views.institution_enroll_student),
    path('institution/enroll/bulk', views.institution_enroll_bulk),
    path('institution/remove', views.institution_removestudent),
    path('institution/remove/bulk', views.institution_removestudent_bulk),
    path('institution/addcourse', views.institution_addcourse),
    path('institution/addcourse/bulk', views.institution_addcourse_bulk),
    path('institution/docreq', views.institution_docreq),
    
    # student
    path('student', views.student),
    path('student/getdocument', views.student_get_docu),
]