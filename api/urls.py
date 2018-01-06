from django.urls import re_path, include
from .views import (
    ListAllUsers,
    RegisterUsers,
    SingleUserDetails,
    ResetUserPassword,
    LoginUser,
    LogoutUser,
    ShoppingLists
    # ManageAPIUsers
)
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'shop_list_api'

# binding view sets to urls explicitly
shopping_lists = ShoppingLists.as_view(actions={
    'get': 'list',
    'post': 'create'
})

shopping_lists_detail = ShoppingLists.as_view(actions={
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    re_path('^auth/register/$',
            RegisterUsers.as_view(),
            name='shop-list-api-register-user'),

    re_path('^auth/reset-password/$',
            ResetUserPassword.as_view(),
            name='shop-list-api-reset-password'),

    re_path('^auth/login/$',
            LoginUser.as_view(),
            name='shop-list-api-login-user'),

    re_path('^auth/logout/$',
            LogoutUser.as_view(),
            name='shop-list-api-logout-user'),

    re_path('^list/users/$',
            ListAllUsers.as_view(),
            name='shop-list-api-all-users'),

    re_path('^users/(?P<username>[\w.@+-]+)/$',
            SingleUserDetails.as_view(),
            name='shop-list-api-user'),

    re_path('^shoppinglists/$',
            shopping_lists,
            name='shop-list-api-shopping-lists'),

    re_path('^shoppinglists/(?P<pk>[0-9]+)/$',
            shopping_lists_detail,
            name='shop-list-api-shopping-lists-detail')
])