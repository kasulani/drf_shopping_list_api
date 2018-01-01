from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
from api.serializers import (
    # UserProfileSerializer,
    # UserSerializer,
    CompositeUserSerializer
)
from api.utils import (
    fetch_all_user_profiles,
    fetch_single_user,
    create_user_profile
)


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
        serializer = CompositeUserSerializer(fetch_all_user_profiles(), many=True)
        return Response(serializer.data)


class ManageAPIUsers(APIView):
    """
    This view is used by admin users to manage users in the system

    Admin users can use this view to; Retrieve, update or delete

    * Requires token authentication
    * Only admin users are able to access this view
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def get(self, request, version, username, format=None):
        """
        Return user profile details for a single user specified
        by the parameter <username>
        """
        data = fetch_single_user(username=username)
        if data is not None:
            serializer = CompositeUserSerializer(data=data)
            serializer.is_valid()
            return Response(data=serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


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

    def get(self, request, version, format='application\json'):
        """
        Retrieve user profile of the user in the request object

        :param request:
        :param version:
        :param username:
        :param format:
        :return:
        """
        data = fetch_single_user(username=request.user.username)
        serializer = CompositeUserSerializer(data=data)
        serializer.is_valid()
        return Response(data=serializer.data)
