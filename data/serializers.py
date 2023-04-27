from rest_framework import serializers
from .models import BloodSugarLog

class BloodSugarLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodSugarLog
        fields = '__all__'
