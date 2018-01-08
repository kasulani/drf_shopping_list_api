from rest_framework import serializers
from api.models import ShoppingList, Item
# from django.contrib.auth.models import User


class CompositeUserSerializer(serializers.Serializer):
    """
    This serializer combines data from django auth user
    and user profile model
    """
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    description = serializers.CharField(max_length=255)
    last_login = serializers.DateTimeField(allow_null=True)
    date_joined = serializers.DateTimeField()


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class ShoppingListSerializer(serializers.ModelSerializer):
    """
    Serializer for the shopping list model
    """
    class Meta:
        model = ShoppingList
        # fields = '__all__'
        exclude = ('user',)


class ItemsSerializer(serializers.ModelSerializer):
    """
    Serializer for the shopping list items model
    """
    class Meta:
        model = Item
        exclude = ('the_list',)

# class UserSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the  User model in django auth
#     """
#     class Meta:
#         model = User
#         fields = '__all__'
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the User Profile model
#     """
#     class Meta:
#         model = UserProfile
#         fields = (
#             'description',
#             'token',
#             'created_on',
#             'updated_on'
#         )
