from api.models import UserProfile
from django.contrib.auth.models import User
from api.serializers import ItemsSerializer

# utility functions and classes


def user_is_permitted(request, username):
    """
    This function returns true if the user in
    request object matches the username provided or
    if the user is super user otherwise returns false

    This function can be used to check if the user in the
    request object is the owner of the account specified
    by username parameter before they do any operation on
    that account

    :param request:
    :param username:
    :return: bool
    """
    return \
        request.user.username == username or request.user.is_superuser


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


def is_safe_to_save(data, user):
    """
    This helper function that inspects the data in the fields
    and updates the corresponding user fields

    :param data:
    :param user:
    :return: bool
    """
    save = False
    if 'email' in data \
            and data['email'] != '':
        user.email = data['email']
        save = True
    if 'password' in data \
            and data['password'] != '':
        user.set_password(data['password'])
        save = True
    if 'first_name' in data \
            and data['first_name'] != '':
        user.first_name = data['first_name']
        save = True
    if 'last_name' in data \
            and data['last_name'] != '':
        user.last_name = data['last_name']
        save = True
    return save


def update_user_profile(data):
    """
    This function updates a user profile
    :return:
    """
    try:
        updated = False
        # find the user to update
        user = User.objects.get(
            username=data['username']
        )
        # update user data
        if is_safe_to_save(data, user):
            user.save()
            updated = True
        # update user profile
        profile = UserProfile.objects.get(user=user)
        if 'description' in data \
                and data['description'] != '':
            profile.description = data['description']
            profile.save()
            updated = True
        return updated
    except Exception:
        return False


def serialize_item(item):
    """
    This function serializes a single
    shopping list item

    :param item:
    :return:
    """
    serializer = ItemsSerializer(data={
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'bought': item.bought
    })
    serializer.is_valid()
    return serializer


def items_results_set(items):
    """
    This functions returns a results set that can be
    serialized

    :param items: raw query set
    :return:
    """
    results = []
    for item in items:
        results.append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'bought': item.bought
        })
    return results
