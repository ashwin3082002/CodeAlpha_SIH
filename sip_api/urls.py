from . import views
from django.urls import path

urlpatterns = [
    path('student/status',views.student_status.as_view()),
    path('student/current',views.current_insti.as_view()),
    path('student/details',views.stu_detail.as_view()),
]

