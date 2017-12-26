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
from api.utils import (
    fetch_all_user_profiles,
    fetch_single_user,
    create_user_profile
)


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

        # compose the data
        data = {
            'username': request.data.get('username', None),
            'email': request.data.get('email', None),
            'password': request.data.get('password', None),
            'first_name': request.data.get('first_name', ''),
            'last_name': request.data.get('last_name', ''),
            'description': request.data.get('description', '')
        }
        # go ahead and create a user profile
        if create_user_profile(data=data):
            # serialize the created user profile
            serializer = CompositeUserSerializer(
                data=fetch_single_user(username=data['username'])
            )
            serializer.is_valid()
            # respond with the created user profile
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

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

        data = fetch_single_user(username=username)
        if data is not None:
            serializer = CompositeUserSerializer(data=data)
            serializer.is_valid()
            return Response(data=serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, version, pk=None):
        # update a single user profile
        return Response({})

    def destroy(self, request, version, pk=None):
        # delete a single user profile
        return Response({})
