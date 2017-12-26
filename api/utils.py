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
