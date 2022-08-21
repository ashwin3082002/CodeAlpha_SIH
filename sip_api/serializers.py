from rest_framework import serializers
from sip_db.models import student_detail

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = student_detail
        fields = ['sid', 'active_status']
