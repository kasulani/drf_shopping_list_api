import json
from rest_framework.views import status
from api.tests.base import AuthBaseTest
from django.urls import reverse


class AuthRegisterUserTest(AuthBaseTest):
    """
    Tests for /auth/register/ endpoint
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


class AuthResetUserPasswordTest(AuthBaseTest):
    """
    Tests for the /auth/reset-password/ endpoint
    """

    def test_reset_user_password_with_valid_data(self):
        # test reset password with valid data
        url = reverse(
            'shop_list_api:shop-list-api-reset-password',
            kwargs={
                'version': 'v1'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.put(
            url,
            data=json.dumps({
                'password': 'some-long-password'
            }),
            content_type='application/json'
        )
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_user_password_with_invalid_data(self):
        # test reset password with invalid data
        url = reverse(
            'shop_list_api:shop-list-api-reset-password',
            kwargs={
                'version': 'v1'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.put(
            url,
            data=json.dumps({
                'pass': 'some-long-password'
            }),
            content_type='application/json'
        )
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthLoginUserTest(AuthBaseTest):
    """
    Tests for the /auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        # test logging in with valid credentials
        url = reverse(
            'shop_list_api:shop-list-api-login-user',
            kwargs={
                'version': 'v1'
            }
        )
        response = self.client.post(
            url,
            data=json.dumps({
                'username': 'test_user',
                'password': 'testing'
            }),
            content_type='application/json'
        )
        # assert token key exists
        self.assertIn('token', response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_with_invalid_credentials(self):
        # test logging in with invalid credentials
        url = reverse(
            'shop_list_api:shop-list-api-login-user',
            kwargs={
                'version': 'v1'
            }
        )
        response = self.client.post(
            url,
            data=json.dumps({
                'username': 'user',
                'password': 'tester'
            }),
            content_type='application/json'
        )
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthLogoutUserTest(AuthBaseTest):
    """
    Tests for the /auth/logout/
    """

    def test_logout_user(self):
        url = reverse(
            'shop_list_api:shop-list-api-logout-user',
            kwargs={
                'version': 'v1'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_user_with_out_login(self):
        url = reverse(
            'shop_list_api:shop-list-api-logout-user',
            kwargs={
                'version': 'v1'
            }
        )
        response = self.client.get(url)
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
