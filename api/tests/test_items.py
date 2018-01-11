import json
from rest_framework.views import status
from api.tests.base import ItemBaseTest
from django.urls import reverse


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
