from rest_framework.test import APITestCase, APIClient
from api.models import UserProfile, ShoppingList
from django.contrib.auth.models import User
from django.urls import reverse
from api.serializers import (
    ShoppingListSerializer,
    CompositeUserSerializer
)
import json


class BaseTest(APITestCase):
    """
    Base Test for Auth endpoints and models
    """

    client = APIClient()
    token = ""

    def setUp(self):
        # create a admin user
        self.user = User.objects.create_superuser(
            username='test_user',
            email='test@mail.com',
            password='testing',
            first_name='test',
            last_name='user',
        )
        # create a user profile for admin user
        self.user_profile = UserProfile.objects.create(
            description='i am a test user',
            user=self.user
        )

        # create a test user with out admin rights
        self.other_user = User.objects.create_user(
            username='other_test_user',
            email='other_test@mail.com',
            password='other_testing',
            first_name='other',
            last_name='user',
        )
        # create a user profile for other test user
        self.other_test_user_profile = UserProfile.objects.create(
            description='i am the other test user',
            user=self.other_user
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

    def login_client(self, username, password):
        # login
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)


class AuthBaseTest(BaseTest):

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


class ShoppingListBaseTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.query_set = ShoppingList.objects.all()
        # create two shopping lists for testing
        self.add_a_shopping_list({
            'name': 'test_list_1',
            'description': 'describe test list 1',
            'user': self.user
        })
        self.add_a_shopping_list({
            'name': 'test_list_2',
            'description': 'describe test list 2',
            'user': self.user
        })

    @staticmethod
    def add_a_shopping_list(data):
        ShoppingList.objects.create(
            name=data.get('name', ''),
            description=data.get('description', ''),
            user=data.get('user', '')
        )

    def get_a_shopping_list_id(self):
        a_list = self.query_set.filter(name="test_list_1")
        return a_list[0].id

    def get_all_shopping_lists(self):
        results = []
        for a_list in self.query_set:
            results.append({
                'id': a_list.id,
                'name': a_list.name,
                'description': a_list.description,
                'created_on': a_list.created_on,
                'updated_on': a_list.updated_on
            })
        return ShoppingListSerializer(results, many=True).data
