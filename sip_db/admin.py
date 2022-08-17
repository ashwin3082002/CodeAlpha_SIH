from django.contrib import admin
from .models import user_detail, institution_detail, degree, course

# register your models here
admin.site.register(user_detail)
admin.site.register(institution_detail)
admin.site.register(degree)
admin.site.register(course)