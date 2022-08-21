from django.shortcuts import render, redirect, HttpResponse
from sip_api.serializers import StudentSerializer
from sip_db.models import institution_detail, student_detail
from django.http import JsonResponse
from sip_db.models import student_detail
# Create your views here.

def index(request):
    s_detial = student_detail.objects.all()
    serializer = StudentSerializer(s_detial, many=True)
    print(serializer.data)
    return JsonResponse({'student' : serializer.data}, safe=False)