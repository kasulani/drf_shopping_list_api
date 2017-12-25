from rest_framework import serializers
from api.models import UserProfile
from django.contrib.auth.models import User


class SingleUserSerializer(serializers.Serializer):
    """
    Serializer for a single user retrieved via the api.
    This serializer combines data from django auth user
    and user profile model
    """
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    description = serializers.CharField(max_length=255)
    last_login = serializers.DateTimeField(allow_null=True)
    date_joined = serializers.DateTimeField()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the  User model in django auth
    """
    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the User Profile model
    """
    class Meta:
        model = UserProfile
        fields = (
            'description',
            'token',
            'created_on',
            'updated_on'
        )