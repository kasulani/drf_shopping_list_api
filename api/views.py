from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import status
from api.serializers import (
    UserProfileSerializer,
    UserSerializer,
    SingleUserSerializer
)
from api.models import UserProfile
from django.contrib.auth.models import User


# Create your views here.


class UserProfileView(viewsets.ViewSet):
    """
    View for the User Profile model
    """

    queryset = UserProfile.objects.all()

    def list(self, request, version):
        # get all user profiles
        serializer = UserProfileSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def create(request, version):
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
        # get details of a single user profile
        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
        except Exception as ex:
            return Response(
                data=ex.message,
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SingleUserSerializer(
            data={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'description': profile.description,
                'last_login': user.last_login,
                'date_joined': user.date_joined
            }
        )
        if serializer.is_valid():
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, version, pk=None):
        # update a single user profile
        return Response({})

    def destroy(self, request, version, pk=None):
        # delete a single user profile
        return Response({})
