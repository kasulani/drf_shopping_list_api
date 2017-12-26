from rest_framework.test import APITestCase, APIClient
from api.models import UserProfile
from django.contrib.auth.models import User
from api.serializers import (
    UserProfileSerializer,
    CompositeUserSerializer
)


class AuthBaseTest(APITestCase):
    """
    Base Test for Auth endpoints and models
    """

    client = APIClient()

    def setUp(self):
        # create a user
        self.user = User.objects.create_user(
            username='test_user',
            email='test@mail.com',
            password='testing',
            first_name='test',
            last_name='user',
        )

        # create a user profile
        self.user_profile = UserProfile.objects.create(
            description='i am a test user',
            user=self.user
        )

        # set token
        self.token = self.user_profile.generate_auth_token(expiration=1)

        # test data
        self.valid_data = {
            # mandatory
            'username': 'another_test_user',
            'email': 'another@mail.com',
            'password': 'another',
            # optional
            'first_name': 'another',
            'last_name': 'user',
            'description': 'yet another test user'
        }

        # if one or more of the mandatory fields is missing, data is invalid
        self.invalid_data = {
            # mandatory
            'username': '',
            'email': 'another@mail.com',
            'password': 'another',
            # optional
            'first_name': '',
            'last_name': '',
            'description': ''
        }

    @staticmethod
    def get_all_expected_user_profiles():
        # get all user profiles in the db and return as a serialized object
        results_queryset = []
        for user in User.objects.all():
            profile = UserProfile.objects.get(user=user)
            results_queryset.append({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'description': profile.description,
                'last_login': user.last_login,
                'date_joined': user.date_joined
            })
        return CompositeUserSerializer(results_queryset, many=True)

    def get_expected_single_user_profile(self):
        # this returns the test user profile
        serializer = CompositeUserSerializer(
            data={
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
                'description': self.user_profile.description,
                'last_login': self.user.last_login,
                'date_joined': self.user.date_joined
            }
        )
        serializer.is_valid()
        return serializer
