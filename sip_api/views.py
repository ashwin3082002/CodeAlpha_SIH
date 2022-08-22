from sip_api.serializers import StudentSerializer, ApikeySerializer
from rest_framework.views import APIView
from sip_db.models import institution_detail, student_detail
from django.http import JsonResponse
from sip_db.models import student_detail, api_details
# Create your views here.

class student_status(APIView):
    def get(self,request,*args,**kwargs):
        sid = self.request.query_params.get("sid")
        api_key = self.request.query_params.get("api_key")
        if api_key == None:
            return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
        else:
            search_details = student_detail.objects.filter(sid = sid).values()
            search_details_api = api_details.objects.filter(api_key=api_key).values()
            serializer = StudentSerializer(search_details, many=True)
            serializer1 = ApikeySerializer(search_details_api, many = True)
            if serializer1.data == []:
                return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
            elif api_key == serializer1.data[0]['api_key']:
                if serializer.data == []:
                    return JsonResponse({'status':'failed','message':'user does not exist'})
                else:
                    data = serializer.data[0]['active_status']
                    if data == "True":
                        return JsonResponse({'status':"success",'student_status' : "Active"}, safe=False)
                    elif data == "False":
                        return JsonResponse({'status':"success",'student_status' : "InActive"}, safe=False)
            else:
                return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})