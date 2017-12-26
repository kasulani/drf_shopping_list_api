from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import status
from api.serializers import (
    UserProfileSerializer,
    UserSerializer,
    CompositeUserSerializer
)
from api.models import UserProfile
from django.contrib.auth.models import User
from api.utils import fetch_all_user_profiles


# Create your views here.


class UserProfileView(viewsets.ViewSet):
    """
    ViewSet for the User Profile. A user profile is a
    combination of data from two models, i.e, the User
    model from django auth and UserProfile model
    """

    queryset = UserProfile.objects.all()

    @staticmethod
    def list(request, version):
        """
        This view function GETs all user profiles
        :param request:
        :param version:
        :return:
        """

        # get all user profiles
        serializer = CompositeUserSerializer(fetch_all_user_profiles(), many=True)
        return Response(serializer.data)

    @staticmethod
    def create(request, version):
        """
        This view function creates/POSTs a new user. A user data is
        stored in two models, i.e, User and UserProfile.
        Therefore the process of creating a user involves two
        steps;
        step 1: create a user account in the django auth User model
        step 2: create a user profile in the UserProfile model
        :param request:
        :param version:
        :return:
        """
        # create a user account and profile
        data = {
            'username': request.data.get('username', None),
            'email': request.data.get('email', None),
            'password': request.data.get('password', None),
            'first_name': request.data.get('first_name', None),
            'last_name': request.data.get('last_name', None)
        }
        # create a user account in the django auth table
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            # save the user account
            serializer.save()
            # create a user profile
            user_profile = UserProfile.objects.create(
                description=request.data.get('description', ''),
                user=User.objects.get_by_natural_key(data['username'])
            )
            serializer = UserProfileSerializer(user_profile)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def retrieve(request, version, username):
        """
        This view function GETs data of a single user
        as a user profile
        :param request: request object
        :param version: api version number
        :param username: username
        :return: serialized user profile
        """

        # first find the user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        # at this point the user exists, find user profile
        profile = UserProfile.objects.get(user=user)
        # serialize the user profile data
        serializer = CompositeUserSerializer(
            data={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'description': profile.description,
                'last_login': user.last_login,
                'date_joined': user.date_joined
            }
        )
        serializer.is_valid()
        # respond with serialized data
        return Response(data=serializer.data)

    def update(self, request, version, pk=None):
        # update a single user profile
        return Response({})

    def destroy(self, request, version, pk=None):
        # delete a single user profile
        return Response({})
