from api.models import UserProfile
from django.contrib.auth.models import User


def fetch_all_user_profiles():
    """
    This function returns a query set that holds
    all user profiles
    :return:
    """
    users_queryset = User.objects.all()
    profiles_queryset = []
    for user in users_queryset:
        profile = UserProfile.objects.get(user=user)
        profiles_queryset.append({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'description': profile.description,
            'last_login': user.last_login,
            'date_joined': user.date_joined
        })
    return profiles_queryset


def fetch_single_user(username):
    """
    This function fetches a single user profile
    :param username:
    :return: data object with user profile data
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    # at this point the user exists, find user profile
    profile = UserProfile.objects.get(user=user)

    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'description': profile.description,
        'last_login': user.last_login,
        'date_joined': user.date_joined
    }
    # the data can be passed to a serializer
    return data


def create_user_profile(data):
    """
    This function creates a user profile
    :return:
    """
    try:
        # create a user in auth
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        # create user profile
        UserProfile.objects.create(
            description=data['description'],
            user=user
        )
        return True
    except Exception:
        return False
