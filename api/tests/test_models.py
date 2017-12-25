from api.tests.base import AuthBaseTest


class UserProfileTest(AuthBaseTest):
    """
    Test User Profile model
    """

    def test_user_profile(self):
        # test if the profile created in the setup exists
        self.assertEqual(self.user_profile.description, 'i am a test user')

    def test_generate_auth_token(self):
        # test if an auth token is generated
        self.assertIsNotNone(self.token)
        self.assertEqual(self.user_profile.token, self.token)

    def test_decode_auth_token(self):
        # test if a valid auth token can be decoded
        decoded = self.user_profile.decode_auth_token(self.token)
        self.assertTrue(decoded['status'])
        self.assertEqual(decoded['details'], 'test_user')

    def test_decode_invalid_auth_token(self):
        # test if an invalid token is decoded
        decoded = self.user_profile.decode_auth_token("EUnjqiwe.iSNAmks.opajsd")
        self.assertFalse(decoded['status'])
        self.assertEqual(decoded['details'], 'Invalid token. Please register or login')
