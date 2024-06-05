from rest_framework import serializers
from .models import CustomNew
from datetime import datetime

class GetCustomNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomNew
        fields = '__all__'

def convert_datetime(datetime_str):
    dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    converted_str = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return converted_str