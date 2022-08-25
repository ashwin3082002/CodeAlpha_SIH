from dataclasses import fields
from rest_framework import serializers
from sip_db.models import api_details, degree, student_detail

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = student_detail
        fields = ['active_status']

class ApikeySerializer(serializers.ModelSerializer):
    class Meta:
        model = api_details
        fields = ["permissions",'api_key']