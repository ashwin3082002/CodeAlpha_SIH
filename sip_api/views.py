from http.client import HTTPResponse
from django.shortcuts import render, redirect, HttpResponse
from sip_api.serializers import StudentSerializer
from rest_framework.views import APIView
from sip_db.models import institution_detail, student_detail
from django.http import JsonResponse
from sip_db.models import student_detail
# Create your views here.

# def student(request):
#     # s_detial = student_detail.objects.all()
#     # serializer = StudentSerializer(s_detial, many=True)
#     # return JsonResponse({'student' : serializer.data}, safe=False)
#     sid = request.query_params.get('sid')
#     print(sid)
#     return HttpResponse("Hello")

class student(APIView):
    def get(self,request,*args,**kwargs):
        sid = self.request.query_params.get("sid")
        search_details = student_detail.objects.filter(sid = sid).values()
        serializer = StudentSerializer(search_details, many=True)
        return JsonResponse({'status':"success",'data' : serializer.data}, safe=False)