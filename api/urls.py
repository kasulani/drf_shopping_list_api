from django.urls import re_path, include
from .views import UserProfileView
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'users', UserProfileView)

app_name = 'shop_list_api'

# I am binding views-sets explicitly to urls instead of using
# the router class because the endpoints have specific urls

# views to manipulate a single user profile
user = UserProfileView.as_view(actions={
    'put': 'update',
    'get': 'retrieve',
    'delete': 'destroy'
})

# views to manipulate all users
all_users = UserProfileView.as_view(actions={
    'get': 'list'
})

# views to register a single user
register_user = UserProfileView.as_view(actions={
    'post': 'create'
})

urlpatterns = [
    re_path('^auth/register/$', register_user, name='shop-list-api-register-user'),
    re_path('^users/$', all_users, name='shop-list-api-all-users'),
    re_path('^users/(?P<username>[\w.@+-]+)/$', user, name='shop-list-api-user'),
]