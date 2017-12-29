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
from api.models import UserProfile
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


class RegisterUser(APIView):
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


class SingleUserDetail(APIView):
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
        Retrieve a single user specified by username

        :param request:
        :param version:
        :param username:
        :param format:
        :return:
        """

        user = None
        try:
            if request.user == User.objects.get(username=username):
                """
                this branch will be executed if the request user matches
                the User object that matches the username parameter
                """
                user = request.user.username
            else:
                """
                this branch will be executed when the request user does not
                match the username parameter. The user requesting to see
                details of another user should be an admin user
                """
                if request.user.is_superuser:
                    user = username

            if user is not None:
                """
                if the user is not None, go ahead attempt to fetch details for the
                user and respond appropriately
                """
                data = fetch_single_user(username=user)
                if data is not None:
                    serializer = CompositeUserSerializer(data=data)
                    serializer.is_valid()
                    return Response(data=serializer.data)
                # return Response(status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
