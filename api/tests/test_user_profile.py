import json
from rest_framework.views import status
from api.tests.base import AuthBaseTest
from django.urls import reverse


class UserProfileTest(AuthBaseTest):
    """
    Tests for the /users/ endpoints
    """

    def test_get_all_user_profiles(self):
        # test if you can get all user profiles
        url = reverse(
            'shop_list_api:shop-list-api-all-users',
            kwargs={'version': 'v1'}
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        serialized = self.get_all_expected_user_profiles()
        # assert data is as expected
        self.assertEqual(response.data, serialized.data)
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_user_profiles_with_a_non_admin_user(self):
        # test if a non admin can retrieve all user profiles
        url = reverse(
            'shop_list_api:shop-list-api-all-users',
            kwargs={'version': 'v1'}
        )
        self.login_client('other_test_user', 'other_testing')
        response = self.client.get(url)
        # assert status code 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_own_user_profile(self):
        # test if you can retrieve a logged in user profile
        url = reverse(
            'shop_list_api:shop-list-api-user',
            kwargs={
                'version': 'v1',
                'username': 'test_user'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        serialized = self.get_expected_single_user_profile()
        # assert that the data is as expected
        self.assertEqual(response.data['first_name'], serialized.data['first_name'])
        self.assertEqual(response.data['last_name'], serialized.data['last_name'])
        self.assertEqual(response.data['email'], serialized.data['email'])
        self.assertEqual(response.data['description'], serialized.data['description'])
        self.assertEqual(response.data['date_joined'], serialized.data['date_joined'])
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_another_user_profile_with_a_non_admin_user(self):
        # test if a non admin can retrieve another user's profile
        url = reverse(
            'shop_list_api:shop-list-api-user',
            kwargs={
                'version': 'v1',
                'username': 'test_user'
            }
        )
        self.login_client('other_test_user', 'other_testing')
        response = self.client.get(url)
        # assert status code 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_own_user_profile(self):
        """
        Test if the logged in user can update their own user profile
        :return:
        """
        url = reverse(
            'shop_list_api:shop-list-api-user',
            kwargs={
                'version': 'v1',
                'username': 'test_user'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.put(
            url,
            data=json.dumps({
                # optional user data
                'email': 'change@mail.com',
                'first_name': 'change',
                'last_name': 'user',
                'description': 'yet another change user'
            }),
            content_type='application/json'
        )
        # assert status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that the data is as expected
        self.assertEqual(response.data['first_name'], "change")
        self.assertEqual(response.data['last_name'], "user")
        self.assertEqual(response.data['email'], "change@mail.com")
        self.assertEqual(response.data['description'], "yet another change user")

    def test_update_a_user_profile_with_non_admin_user(self):
        # test if a non admin can update another user's profile
        url = reverse(
            'shop_list_api:shop-list-api-user',
            kwargs={
                'version': 'v1',
                'username': 'test_user'
            }
        )
        self.login_client('other_test_user', 'other_testing')
        response = self.client.put(
            url,
            data=json.dumps({
                # optional user data
                'email': 'change@mail.com',
                'first_name': 'change',
                'last_name': 'user',
                'description': 'yet another change user'
            }),
            content_type='application/json'
        )
        # assert status code 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_a_non_existing_user_profile(self):
        """
        Test if admin user can update non existing user
        :return:
        """
        url = reverse(
            'shop_list_api:shop-list-api-user',
            kwargs={
                'version': 'v1',
                'username': 'tester_user'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.put(
            url,
            data=json.dumps({
                # optional user data
                'email': 'change@mail.com',
                'first_name': 'change',
                'last_name': 'user',
                'description': 'yet another change user'
            }),
            content_type='application/json'
        )
        # assert status code is 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_a_single_non_existing_user_profile(self):
        # test if admin user can retrieve a non existing single user profile
        # by supplying an invalid username in the url
        url = reverse(
            'shop_list_api:shop-list-api-user',
            kwargs={
                'version': 'v1',
                'username': 'testuser'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_a_single_existing_user_profile(self):
        # test if admin user can retrieve a existing single user profile
        # by supplying an invalid username in the url
        url = reverse(
            'shop_list_api:shop-list-api-user',
            kwargs={
                'version': 'v1',
                'username': 'test_user'
            }
        )
        self.login_client('test_user', 'testing')
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
