from rest_framework.views import status
from api.tests.base import AuthBaseTest
from django.urls import reverse
import json


class UserProfileTest(AuthBaseTest):
    """
    Tests for the /users/ endpoints
    """

    def test_get_all_user_profile(self):
        # test if you can get all user profiles
        url = reverse(
            'shop_list_api:shop-list-api-all-users',
            kwargs={'version': 'v1'}
        )
        self.login_client()
        response = self.client.get(url)
        serialized = self.get_all_expected_user_profiles()
        # assert data is as expected
        self.assertEqual(response.data, serialized.data)
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_own_user_profile(self):
        # test if you can retrieve a logged in user profile
        url = reverse(
            'shop_list_api:shop-list-api-user',
            kwargs={
                'version': 'v1'
            }
        )
        self.login_client()
        response = self.client.get(url)
        serialized = self.get_expected_single_user_profile()
        # assert that the data is as expected
        self.assertEqual(response.data[0]['first_name'], serialized.data['first_name'])
        self.assertEqual(response.data[0]['last_name'], serialized.data['last_name'])
        self.assertEqual(response.data[0]['email'], serialized.data['email'])
        self.assertEqual(response.data[0]['description'], serialized.data['description'])
        self.assertEqual(response.data[0]['date_joined'], serialized.data['date_joined'])
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_single_non_existing_user_profile(self):
        # test if admin user can retrieve a non existing single user profile
        # by supplying an invalid username in the url
        url = reverse(
            'shop_list_api:shop-list-manage-user',
            kwargs={
                'version': 'v1',
                'username': 'testuser'
            }
        )
        self.login_client()
        response = self.client.get(url)
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_a_single_existing_user_profile(self):
        # test if admin user can retrieve a existing single user profile
        # by supplying an invalid username in the url
        url = reverse(
            'shop_list_api:shop-list-manage-user',
            kwargs={
                'version': 'v1',
                'username': 'test_user'
            }
        )
        self.login_client()
        response = self.client.get(url)
        serialized = self.get_expected_single_user_profile()
        # assert data is as expected
        self.assertEqual(response.data['first_name'], serialized.data['first_name'])
        self.assertEqual(response.data['last_name'], serialized.data['last_name'])
        self.assertEqual(response.data['email'], serialized.data['email'])
        self.assertEqual(response.data['description'], serialized.data['description'])
        self.assertEqual(response.data['date_joined'], serialized.data['date_joined'])
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthRegisterUserTest(AuthBaseTest):
    """
    Tests for /auth/register endpoint
    """
    def test_create_a_user_profile_with_valid_data(self):
        # test creating a user with valid data
        url = reverse(
            'shop_list_api:shop-list-api-register-user',
            kwargs={
                'version': 'v1'
            }
        )
        response = self.client.post(
            url,
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        # assert status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_a_user_profile_with_invalid_data(self):
        # test creating a user with invalid data
        url = reverse(
            'shop_list_api:shop-list-api-register-user',
            kwargs={
                'version': 'v1'
            }
        )
        response = self.client.post(
            url,
            data=json.dumps(self.invalid_data),
            content_type='application/json'
        )
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
