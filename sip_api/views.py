from unittest import result
from sip_api.serializers import StudentSerializer, ApikeySerializer
from rest_framework.views import APIView
from sip_db.models import account_detail, degree, institution_detail, student_detail
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
            try:
                perm = search_details_api[0]['permissions']
            except:
                return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
            if perm == 'status': 
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
            else:
                return JsonResponse({'status':'Permission Denied',"message":"You Don't Have permission to query this API"})

class current_insti(APIView):
    def get(self,request,*args,**kwargs):
        sid = self.request.query_params.get("sid")
        api_key = self.request.query_params.get("api_key")
        if api_key == None:
            return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
        else:
            search_details_api = api_details.objects.filter(api_key=api_key).values()
            try:
                perm = search_details_api[0]['permissions']
            except:
                return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
            if perm == "institution":
                serializer1 = ApikeySerializer(search_details_api, many = True)
                d = degree.objects.filter(sid=sid, status = 'Pursuing').values()
                if serializer1.data==[]:
                    return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
                elif api_key == serializer1.data[0]['api_key']:
                    if d:
                        iid_dict={}
                        for i in range(len(d)):
                            iid = d[i]['iid_id']
                            nam = institution_detail.objects.get(id = iid).name
                            iid_dict[iid]=nam  
                        result_dict = {"Status":"Success"}
                        result_dict['data']=iid_dict
                        return JsonResponse(result_dict)
                    else:
                        return JsonResponse({"Status":"Failed"})
            else:
                return JsonResponse({'status':'Permission Denied',"message":"You Don't Have permission to query this API"})

class stu_detail(APIView):
    def get(self,request,*args,**kwargs):
        sid = self.request.query_params.get("sid")
        api_key = self.request.query_params.get("api_key")
        if api_key == None:
            return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
        else:
            search_details_api = api_details.objects.filter(api_key=api_key).values()
            try:
                perm = search_details_api[0]['permissions']
            except:
                return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
            if perm == 'details':
                serializer1 = ApikeySerializer(search_details_api, many = True)
                if serializer1.data == []:
                    return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
                elif api_key == serializer1.data[0]['api_key']:
                    d = student_detail.objects.filter(sid=sid).values()
                    if d:
                        d=d[0]
                        result_dict = {"Status":"Success"}
                        result_dict['data'] = d
                        return JsonResponse(result_dict)
                    else:
                        return JsonResponse({"Status":"Failed","Message":"SID Doesn't Exists"})
            else:
                return JsonResponse({'status':'Permission Denied',"message":"You Don't Have permission to query this API"})

class bank_account(APIView):
    def get(self,request,*args,**kwargs):
        sid = self.request.query_params.get("sid")
        api_key = self.request.query_params.get("api_key")
        if api_key == None:
            return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
        else:
            search_details_api = api_details.objects.filter(api_key=api_key).values()
            try:
                perm = search_details_api[0]['permissions']
            except:
                return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
            if perm == 'bank':
                serializer1 = ApikeySerializer(search_details_api, many = True)
                if serializer1.data == []:
                    return JsonResponse({'status':'Permission Denied',"message":"You are not authorized to use this API"})
                elif api_key == serializer1.data[0]['api_key']:
                    search_details = account_detail.objects.filter(sid=sid).values()
                    if search_details:
                        search_details=search_details[0]
                        result_dict = {"Status":"Success"}
                        result_dict['data'] = search_details
                        return JsonResponse(result_dict)
                    else:
                        return JsonResponse({"Status":"Failed","Message":"Bank Details Does'nt Exists for the SID"})
            else:
                return JsonResponse({'status':'Permission Denied',"message":"You Don't Have permission to query this API"})
