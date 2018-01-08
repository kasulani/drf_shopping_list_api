from rest_framework.views import status
from api.tests.base import (
    AuthBaseTest,
    ShoppingListBaseTest,
    ItemBaseTest
)
from django.urls import reverse
import json


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


class ShoppingListsTest(ShoppingListBaseTest):
    """
    Tests for the /shoppinglists/
    """

    def test_get_all_shopping_lists(self):
        # test getting all lists with a registered user
        url = reverse(
            'shop_list_api:shop-list-api-shopping-lists',
            kwargs={
                'version': 'v1'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        # assert data is as expected
        self.assertEqual(response.data, self.get_all_shopping_lists())
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_shopping_lists_with_anonymous_user(self):
        # test getting all lists with an anonymous user
        url = reverse(
            'shop_list_api:shop-list-api-shopping-lists',
            kwargs={
                'version': 'v1'
            }
        )
        response = self.client.get(url)
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_a_shopping_list(self):
        url = reverse(
            'shop_list_api:shop-list-api-shopping-lists-detail',
            kwargs={
                'version': 'v1',
                'pk': self.get_a_shopping_list_id()
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        # assert data is as expected
        self.assertEqual(response.data['name'], 'test_list_1')
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_non_existing_shopping_list_id(self):
        url = reverse(
            'shop_list_api:shop-list-api-shopping-lists-detail',
            kwargs={
                'version': 'v1',
                'pk': 201
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        # assert status code is 404 NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_a_shopping_list_with_valid_data(self):
        url = reverse(
            'shop_list_api:shop-list-api-shopping-lists',
            kwargs={
                'version': 'v1'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.post(
            url,
            data=json.dumps({
                'name': 'test_list_3',
                'description': 'describe test list 3'
            }),
            content_type='application/json'
        )
        # assert data is as expected
        self.assertEqual(response.data['name'], 'test_list_3')
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_a_shopping_list_with_invalid_data(self):
        url = reverse(
            'shop_list_api:shop-list-api-shopping-lists',
            kwargs={
                'version': 'v1'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.post(
            url,
            data=json.dumps({}),
            content_type='application/json'
        )
        # assert status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_an_existing_shopping_list(self):
        url = reverse(
            'shop_list_api:shop-list-api-shopping-lists-detail',
            kwargs={
                'version': 'v1',
                'pk': self.get_a_shopping_list_id()
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.put(
            url,
            data=json.dumps({
                'name': 'test_list_4',
                'description': 'describe test list 4'
            }),
            content_type='application/json'
        )
        # assert data is as expected
        self.assertEqual(response.data['name'], 'test_list_4')
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_a_non_existing_shopping_list(self):
        url = reverse(
            'shop_list_api:shop-list-api-shopping-lists-detail',
            kwargs={
                'version': 'v1',
                'pk': 600
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.put(
            url,
            data=json.dumps({
                'name': 'test_list_4',
                'description': 'describe test list 4'
            }),
            content_type='application/json'
        )
        # assert status code is 404 NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_an_existing_shopping_list(self):
        url = reverse(
            'shop_list_api:shop-list-api-shopping-lists-detail',
            kwargs={
                'version': 'v1',
                'pk': self.get_a_shopping_list_id()
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.delete(url)
        # assert status code is 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_a_non_existing_shopping_list(self):
        url = reverse(
            'shop_list_api:shop-list-api-shopping-lists-detail',
            kwargs={
                'version': 'v1',
                'pk': 300
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.delete(url)
        # assert status code is 404 NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ItemsTest(ItemBaseTest):
    """
    Tests for the /shoppinglists/items/
    """

    def test_get_all_items(self):
        # test getting all lists with a registered user
        url = reverse(
            'shop_list_api:shopping-lists-all-items',
            kwargs={
                'version': 'v1'
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        # assert data is as expected
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.get_shopping_list_item()['name'])
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_items_on_a_List(self):
        # test retrieving all items on a given list
        url = reverse(
            'shop_list_api:shopping-lists-items',
            kwargs={
                'version': 'v1',
                'list_id': self.get_a_shopping_list_id(),
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        # assert data is as expected
        self.assertEqual(len(response.data), 1)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_items_on_a_non_existing_List(self):
        # test retrieving all items on a non existing list
        url = reverse(
            'shop_list_api:shopping-lists-items',
            kwargs={
                'version': 'v1',
                'list_id': 77,
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        # assert that the return array is empty
        self.assertEqual(len(response.data), 0)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_an_existing_item(self):
        # test retrieve an item on a specific list
        url = reverse(
            'shop_list_api:shopping-lists-items-detail',
            kwargs={
                'version': 'v1',
                # 'list_id': self.get_a_shopping_list_id(),
                'item_id': self.get_a_item_id()
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        # assert data is as expected
        self.assertEqual(response.data['name'], self.get_shopping_list_item()['name'])
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_non_existing_item(self):
        # test retrieve a non existing
        url = reverse(
            'shop_list_api:shopping-lists-items-detail',
            kwargs={
                'version': 'v1',
                'item_id': 90
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.get(url)
        # assert status code is 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_an_item(self):
        # test adding an item to an existing shopping list
        url = reverse(
            'shop_list_api:shopping-lists-items',
            kwargs={
                'version': 'v1',
                'list_id': self.get_a_shopping_list_id()
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.post(
            url,
            data=json.dumps({
                'name': 'test item 2',
                'description': 'this is a test item'
            }),
            content_type='application/json'
        )
        # assert data is as expected
        self.assertEqual(response.data['name'], 'test item 2')
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_an_item_with_invalid_data(self):
        # test adding an item to an existing shopping list using
        # invalid data such as a missing item name
        url = reverse(
            'shop_list_api:shopping-lists-items',
            kwargs={
                'version': 'v1',
                'list_id': self.get_a_shopping_list_id()
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.post(
            url,
            data=json.dumps({
                'name': '',
                'description': ''
            }),
            content_type='application/json'
        )
        # assert status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_an_item_to_non_existing_list(self):
        # test adding an item to a non existing list
        url = reverse(
            'shop_list_api:shopping-lists-items',
            kwargs={
                'version': 'v1',
                'list_id': 900
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.post(
            url,
            data=json.dumps({
                'name': 'test item 2',
                'description': 'this is a test item'
            }),
            content_type='application/json'
        )
        # assert status code is 404 NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_an_item(self):
        # test updating an existing item on an existing list
        url = reverse(
            'shop_list_api:shopping-lists-items-detail',
            kwargs={
                'version': 'v1',
                # 'list_id': self.get_a_shopping_list_id(),
                'item_id': self.get_a_item_id()
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.put(
            url,
            data=json.dumps({
                'name': 'test item 4',
                'description': 'this is a test update item'
            }),
            content_type='application/json'
        )
        # assert data is as expected
        self.assertEqual(response.data['name'], 'test item 4')
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_an_item_with_invalid_data(self):
        # test updating an existing item on an existing list
        # with invalid data
        url = reverse(
            'shop_list_api:shopping-lists-items-detail',
            kwargs={
                'version': 'v1',
                'item_id': self.get_a_item_id()
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.put(
            url,
            data=json.dumps({
                'name': '',
                'description': ''
            }),
            content_type='application/json'
        )
        # assert status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_a_non_existing_item(self):
        # test updating a non existing item on an existing list
        url = reverse(
            'shop_list_api:shopping-lists-items-detail',
            kwargs={
                'version': 'v1',
                # 'list_id': self.get_a_shopping_list_id(),
                'item_id': 200
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.put(
            url,
            data=json.dumps({
                'name': 'test item 5',
                'description': 'this is a test update item'
            }),
            content_type='application/json'
        )
        # assert status code is 404 NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_an_existing_item(self):
        # test deleting an existing item on an existing list
        url = reverse(
            'shop_list_api:shopping-lists-items-detail',
            kwargs={
                'version': 'v1',
                # 'list_id': self.get_a_shopping_list_id(),
                'item_id': self.get_a_item_id()
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.delete(url)
        # assert status code is 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_a_non_existing_item(self):
        # test deleting a non existing item on an existing list
        url = reverse(
            'shop_list_api:shopping-lists-items-detail',
            kwargs={
                'version': 'v1',
                # 'list_id': self.get_a_shopping_list_id(),
                'item_id': 17
            }
        )
        self.login_client('test_user', 'testing')
        response = self.client.delete(url)
        # assert status code is 404 NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
