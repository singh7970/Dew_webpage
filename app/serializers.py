from rest_framework import serializers
from .models import Register
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Include all fields

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user