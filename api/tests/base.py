from rest_framework.test import APITestCase, APIClient
from api.models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
from api.serializers import (
    # UserProfileSerializer,
    CompositeUserSerializer
)
import json


class AuthBaseTest(APITestCase):
    """
    Base Test for Auth endpoints and models
    """

    client = APIClient()
    token = ""

    def setUp(self):
        # create a user
        self.user = User.objects.create_superuser(
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

        # test data
        self.valid_data = {
            # mandatory
            'username': 'another_test_user',
            'password': 'another',
            # optional
            'email': 'another@mail.com',
            'first_name': 'another',
            'last_name': 'user',
            'description': 'yet another test user'
        }

        # if one or more of the mandatory fields is missing,
        # data is invalid
        self.invalid_data = {
            # mandatory
            'username': '',
            'password': '',
            # optional
            'email': 'another@mail.com',
            'first_name': '',
            'last_name': '',
            'description': ''
        }

    def login_client(self):
        # login
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': 'test_user',
                    'password': 'testing'
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username='test_user', password='testing')

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
