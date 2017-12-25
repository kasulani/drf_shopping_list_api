from rest_framework.views import status
from api.tests.base import AuthBaseTest
from django.urls import reverse


class UserProfileViewTest(AuthBaseTest):
    """
    Tests for the user profile CRUD endpoints
    """

    def test_get_all_user_profile(self):
        # test if you can get all user profiles
        url = reverse(
            'shop_list_api:shop-list-api-all-users',
            kwargs={'version': 'v1'}
        )
        response = self.client.get(url)
        serialized = self.get_all_expected_user_profiles()
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_single_user_profile(self):
        # test if you can retrieve a single user profile
        # by supplying a username in the url
        url = reverse(
            'shop_list_api:shop-list-api-user',
            kwargs={
                'version': 'v1',
                'username': 'test_user'
            }
        )
        response = self.client.get(url)
        serialized = self.get_expected_single_user_profile()
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
            data=self.valid_data,
            content_type='application/json'
        )
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
                data=self.invalid_data,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
