from django.contrib import admin
from .models import student_detail, institution_detail, degree, course, docreq, api_details, account_detail, institution_id, student_id

# register your models here
admin.site.register(student_detail)
admin.site.register(institution_detail)
admin.site.register(degree)
admin.site.register(course)
admin.site.register(docreq)
admin.site.register(api_details)
admin.site.register(account_detail)
admin.site.register(institution_id)
admin.site.register(student_id)
