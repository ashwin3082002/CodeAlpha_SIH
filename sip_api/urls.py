from . import views
from django.urls import path, include

urlpatterns = [
    path('student/status',views.student_status.as_view()),
]

