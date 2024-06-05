from rest_framework import serializers
from .models import CustomNew

class GetCustomNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomNew
        fields = '__all__'