from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegisterLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "role", "last_name", "first_name", "phone")
        read_only_fields = ("id", "email", "role")
