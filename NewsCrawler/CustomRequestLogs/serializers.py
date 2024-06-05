from rest_framework import serializers
from .models import CustomRequestLog

class GetCustomRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRequestLog
        fields = '__all__'
