import json
from rest_framework.views import status
from api.tests.base import ShoppingListBaseTest
from django.urls import reverse


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
        self.assertEqual(len(response.data), len(self.get_all_shopping_lists()))
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

