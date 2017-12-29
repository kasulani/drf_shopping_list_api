from django.urls import re_path
from .views import (
    ListAllUsers,
    RegisterUser,
    SingleUserDetail
)
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'shop_list_api'

urlpatterns = format_suffix_patterns([
    re_path('^auth/register/$', RegisterUser.as_view(), name='shop-list-api-register-user'),
    re_path('^users/$', ListAllUsers.as_view(), name='shop-list-api-all-users'),
    re_path('^users/(?P<username>[\w.@+-]+)/$', SingleUserDetail.as_view(), name='shop-list-api-user'),
])