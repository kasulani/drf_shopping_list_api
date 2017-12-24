from django.test import TestCase
from api.models import UserProfile
from django.contrib.auth.models import User


class UserProfileTest(TestCase):
    """
    Test User Profile model
    """
    user = None
    user_profile = None
    token = None

    def setUp(self):
        # create a user
        self.user = User.objects.create_user(
            username='test_user',
            email='test@mail.com',
            password='testing')
        # create a user profile
        self.user_profile = UserProfile.objects.create(
            first_name='test',
            last_name='user',
            description='i am a test user',
            user=self.user
        )
        # set token
        self.token = self.user_profile.generate_auth_token(expiration=1)

    def test_user_profile(self):
        # test if the profile created in the setup exists
        self.assertEqual(self.user_profile.first_name, 'test')
        self.assertEqual(self.user_profile.last_name, 'user')
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
