from rest_framework import serializers
from .models import CustomRequestLog
from CustomUsers.serializers import GetCustomUserProfileSerializer

class GetCustomRequestLogSerializer(serializers.ModelSerializer):
    owner = GetCustomUserProfileSerializer()
    class Meta:
        model = CustomRequestLog
        fields = '__all__'
