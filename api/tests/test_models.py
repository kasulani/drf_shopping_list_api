from api.tests.base import AuthBaseTest, ShoppingListBaseTest


class UserProfileTest(AuthBaseTest):
    """
    Test User Profile model
    """

    def test_user_profile(self):
        # test if the profile created in the setup exists
        self.assertEqual(self.user_profile.description, 'i am a test user')


class ShoppingListTest(ShoppingListBaseTest):
    """
    Test ShoppingList model
    """

    def test_shopping_list(self):
        a_list = self.query_set[0]
        self.assertEqual(a_list.name, 'test_list_1')
        self.assertEqual(a_list.description, 'describe test list 1')
