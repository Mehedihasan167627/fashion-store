from .models import CustomUser
from rest_framework import serializers

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=CustomUser
        fields=["email","password"]
