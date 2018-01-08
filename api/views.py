from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework import viewsets
from rest_framework.generics import (
    UpdateAPIView,
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.serializers import (
    # UserProfileSerializer,
    ShoppingListSerializer,
    ItemsSerializer,
    CompositeUserSerializer,
    TokenSerializer
)
from api.utils import (
    fetch_all_user_profiles,
    fetch_single_user,
    create_user_profile,
    update_user_profile,
    user_is_permitted,
    serialize_item,
    items_results_set
)
from api.models import ShoppingList, Item
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# API endpoint views

class ListAllUsers(APIView):
    """
    View to list all users in the system

    * Requires token authentication
    * Only admin users are able to access this view
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def get(self, request, version, format=None):
        """
        Return a list of all users.
        """
        serializer = CompositeUserSerializer(
            fetch_all_user_profiles(),
            many=True
        )
        return Response(serializer.data)


class RegisterUsers(APIView):
    """
    View to create a user in the system

    * this is a public view
    * non authenticated users can access it
    """
    permission_classes = (AllowAny,)

    def post(self, request, version, format='json'):
        """
        Create a new user

        This view function creates/POSTs a new user. A user data is
        stored in two models, i.e, User and UserProfile.
        Therefore the process of creating a user involves two
        steps;
        step 1: create a user account in the django auth User model
        step 2: create a user profile in the UserProfile model

        :param request:
        :param version:
        :param format:
        :return:
        """
        # compose the data
        data = {
            'username': request.data.get('username', None),
            'email': request.data.get('email', None),
            'password': request.data.get('password', None),
            'first_name': request.data.get('first_name', ''),
            'last_name': request.data.get('last_name', ''),
            'description': request.data.get('description', '')
        }
        # go ahead and create a user profile
        if create_user_profile(data=data):
            # serialize the created user profile
            serializer = CompositeUserSerializer(
                data=fetch_single_user(username=data['username'])
            )
            serializer.is_valid()
            # respond with the created user profile
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SingleUserDetails(APIView):
    """
    Retrieve, update or delete a user instance.

    * Requires token authentication
    * Only owner of account can view own details
    * admin users can view details of other users
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None, **kwargs):
        """
        Retrieve user profile of the user in the request object

        :param request:
        :param version:
        :param username:
        :param format:
        :return:
        """
        username = kwargs['username']
        if user_is_permitted(request, username):
            data = fetch_single_user(username=username)
            if data is not None:
                serializer = CompositeUserSerializer(data=data)
                serializer.is_valid()
                return Response(data=serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=None, **kwargs):
        """
        Update user profile of the user in the request object

        :param request:
        :param format:
        :return:
        """
        username = kwargs['username']
        if user_is_permitted(request, username):
            data = {
                'username': username,
                'email': request.data.get('email', ''),
                'first_name': request.data.get('first_name', ''),
                'last_name': request.data.get('last_name', ''),
                'description': request.data.get('description', '')
            }
            if update_user_profile(data=data):
                serializer = CompositeUserSerializer(
                    data=fetch_single_user(
                        username=request.user.username
                    )
                )
                serializer.is_valid()
                return Response(data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ResetUserPassword(UpdateAPIView):
    """
    View to update password of a logged in user
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        """
        Update password of the user in the request object

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = {
            'username': request.user.username,
            'password': request.data.get('password', '')
        }
        if update_user_profile(data=data):
            return Response(status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginUser(CreateAPIView):
    """
    View to login a user

    returns a token
    """
    permission_classes = (AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                'token': jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutUser(ListAPIView):
    """
    View to logout a user.

    * You have to have logged in to be able logout
    """

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ShoppingLists(viewsets.ModelViewSet):
    """
    Shopping Lists CRUD endpoints
    """

    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO: Admin user can view all shopping lists
    # TODO: pagination

    def list(self, request, *args, **kwargs):
        """
        get all shopping lists as per user logged in

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        lists = self.queryset.filter(user=request.user)
        results = []
        for a_list in lists:
            results.append({
                'id': a_list.id,
                'name': a_list.name,
                'description': a_list.description
            })
        return Response(ShoppingListSerializer(results, many=True).data)

    def create(self, request, *args, **kwargs):
        """
        Adds a new shopping list

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        name = request.data.get('name', '')
        if not name:  # shopping list name is mandatory
            return Response(status=status.HTTP_400_BAD_REQUEST)

        new_list = ShoppingList.objects.create(
            name=name,
            description=request.data.get('description', ''),
            user=request.user
        )
        serializer = ShoppingListSerializer(
            data={
                'name': new_list.name,
                'description': new_list.description
            })
        serializer.is_valid()
        return Response(
            data=serializer.data
        )


class ListAllItems(ListAPIView):
    """
    List all items that belong to a user
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        items = Item.objects.raw(
            "select api_item.id, api_item.name, api_item.description, "
            "api_item.bought, api_shoppinglist.name, auth_user.first_name "
            "from api_item "
            "join api_shoppinglist "
            "on api_shoppinglist.id=api_item.the_list_id "
            "join auth_user "
            "on auth_user.id=api_shoppinglist.user_id where auth_user.id=%s",
            [request.user.id]
        )
        return Response(ItemsSerializer(
            items_results_set(items),
            many=True).data)


class ItemsListCreate(ListCreateAPIView):
    """
    View to list and create items of/for a logged in user
    """

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Return all items for the logged in user

        :param request:
        :param kwargs:
        :return:
        """
        items = Item.objects.raw(
            "select * from api_item where "
            "api_item.the_list_id=%s",
            [kwargs['list_id']]
        )
        results = []
        for item in items:
            results.append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'bought': item.bought
            })
        return Response(ItemsSerializer(
            items_results_set(items),
            many=True).data)

    def post(self, request, *args, **kwargs):
        """
        Create a new item on a given list

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            the_list = ShoppingList.objects.get(id=kwargs['list_id'])
            name = request.data.get('name', '')
            if not name:  # item name is mandatory
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item = Item.objects.create(
                name=name,
                description=request.data.get('description', ''),
                the_list=the_list
            )
            return Response(serialize_item(item).data)
        except ShoppingList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ItemsDetails(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, delete an item
    """

    queryset = Item.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        retrieve a specific item on a given list

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        item_id = kwargs['item_id']
        try:
            item = Item.objects.get(id=item_id)
            return Response(serialize_item(item).data)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        """
        update a item

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            item = Item.objects.get(id=kwargs['item_id'])
            name = request.data.get('name', '')
            if not name:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item.name = name
            item.description = request.data.get('description', '')
            item.bought = request.data.get('bought', 0)
            item.save()
            return Response(serialize_item(item).data)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        """
        Delete an item

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            item = Item.objects.get(id=kwargs['item_id'])
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)