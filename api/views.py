from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.generics import (
    UpdateAPIView,
    CreateAPIView,
    ListAPIView
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.serializers import (
    # UserProfileSerializer,
    # UserSerializer,
    CompositeUserSerializer,
    TokenSerializer
)
from api.utils import (
    fetch_all_user_profiles,
    fetch_single_user,
    create_user_profile,
    update_user_profile,
    user_is_permitted
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# API endpoint views

class ListAllUsers(APIView):
    """
    View to list all users in the system

    * Requires token authentication
    * Only admin users are able to access this view
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def get(self, request, version, format=None):
        """
        Return a list of all users.
        """
        serializer = CompositeUserSerializer(
            fetch_all_user_profiles(),
            many=True
        )
        return Response(serializer.data)


class RegisterUsers(APIView):
    """
    View to create a user in the system

    * this is a public view
    * non authenticated users can access it
    """
    permission_classes = (AllowAny,)

    def post(self, request, version, format='json'):
        """
        Create a new user

        This view function creates/POSTs a new user. A user data is
        stored in two models, i.e, User and UserProfile.
        Therefore the process of creating a user involves two
        steps;
        step 1: create a user account in the django auth User model
        step 2: create a user profile in the UserProfile model

        :param request:
        :param version:
        :param format:
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


class SingleUserDetails(APIView):
    """
    Retrieve, update or delete a user instance.

    * Requires token authentication
    * Only owner of account can view own details
    * admin users can view details of other users
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, version, username, format=None):
        """
        Retrieve user profile of the user in the request object

        :param request:
        :param version:
        :param username:
        :param format:
        :return:
        """
        if user_is_permitted(request, username):
            data = fetch_single_user(username=username)
            if data is not None:
                serializer = CompositeUserSerializer(data=data)
                serializer.is_valid()
                return Response(data=serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, version, username, format=None):
        """
        Update user profile of the user in the request object

        :param request:
        :param version:
        :param username:
        :param format:
        :return:
        """
        if user_is_permitted(request, username):
            data = {
                'username': username,
                'email': request.data.get('email', ''),
                'first_name': request.data.get('first_name', ''),
                'last_name': request.data.get('last_name', ''),
                'description': request.data.get('description', '')
            }
            if update_user_profile(data=data):
                serializer = CompositeUserSerializer(
                    data=fetch_single_user(
                        username=request.user.username
                    )
                )
                serializer.is_valid()
                return Response(data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ResetUserPassword(UpdateAPIView):
    """
    View to update password of a logged in user
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        """
        Update password of the user in the request object

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = {
            'username': request.user.username,
            'password': request.data.get('password', '')
        }
        if update_user_profile(data=data):
            return Response(status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginUser(CreateAPIView):
    """
    View to login a user

    returns a token
    """
    permission_classes = (AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                'token': jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutUser(ListAPIView):
    """
    View to logout a user.

    * You have to have logged in to be able logout
    """

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)