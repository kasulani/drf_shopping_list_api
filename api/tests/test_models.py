from api.tests.base import AuthBaseTest


class UserProfileTest(AuthBaseTest):
    """
    Test User Profile model
    """

    def test_user_profile(self):
        # test if the profile created in the setup exists
        self.assertEqual(self.user_profile.description, 'i am a test user')