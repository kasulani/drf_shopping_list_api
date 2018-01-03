from django.urls import re_path, include
from .views import (
    ListAllUsers,
    RegisterUsers,
    SingleUserDetails,
    ResetUserPassword,
    LoginUser,
    LogoutUser
    # ManageAPIUsers
)
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'shop_list_api'

urlpatterns = format_suffix_patterns([
    re_path('^auth/register/$', RegisterUsers.as_view(), name='shop-list-api-register-user'),
    re_path('^auth/reset-password/$', ResetUserPassword.as_view(), name='shop-list-api-reset-password'),
    re_path('^auth/login/$', LoginUser.as_view(), name='shop-list-api-login-user'),
    re_path('^auth/logout/$', LogoutUser.as_view(), name='shop-list-api-logout-user'),
    re_path('^list/users/$', ListAllUsers.as_view(), name='shop-list-api-all-users'),
    re_path('^users/(?P<username>[\w.@+-]+)/$', SingleUserDetails.as_view(), name='shop-list-api-user')
])