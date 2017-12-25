import jwt
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.conf import settings

# Create your models here.


class UserProfile(models.Model):
    """
    User Profile model
    This model extends the user model provided by django auth
    """

    # one sentence description about the user
    description = models.CharField(max_length=255, null=True)
    # JWT token set after authentication of user
    token = models.CharField(max_length=255, null=True)
    # when the user profile was updated
    created_on = models.DateTimeField(auto_now_add=True)
    # when the user profile was last updated
    updated_on = models.DateTimeField(auto_now=True)
    # one to one field to the User model in django auth
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def generate_auth_token(self, expiration=50):
        """
        This method generates an auth token. It saves the generated
        token in the token field of the this model and returns that
        token when called as a function
        :param expiration: sets the validity period for the token
        :return: token
        """
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=expiration),
            'iat': datetime.utcnow(),
            'sub': self.user.username
        }
        # create the byte string token using the payload and the SECRET key
        jwt_string = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        # update the token field of the user profile model
        self.token = jwt_string
        self.save()

        # return the token string to the caller
        return jwt_string

    @staticmethod
    def decode_auth_token(token):
        """
        Decodes the access token from the Authorization header.
        :return: a dictionary
        """
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, settings.SECRET_KEY)
            return {
                'status': True,
                'details': payload['sub']
            }
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return {
                'status': False,
                'details': "Expired token. Please login to get a new token"
            }
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return {
                'status': False,
                'details': "Invalid token. Please register or login"
            }

    def __repr__(self):
        # this is the string representation of the UserProfile object
        user = self.user.objects.all()
        return '<User: %s>' % user.username