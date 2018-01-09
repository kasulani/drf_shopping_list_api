from api.models import ShoppingList, Item
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from api.serializers import ItemsSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.utils import (
    serialize_item,
    items_results_set
)
from rest_framework.pagination import PageNumberPagination


class ListAllItems(ListAPIView):
    """
    List all items that belong to a user
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        """
        Example select statement on multiple tables
        using join

        SELECT TableA.*, TableB.*, TableC.*, TableD.*
        FROM TableA
            JOIN TableB
                ON TableB.aID = TableA.aID
            JOIN TableC
                ON TableC.cID = TableB.cID
            JOIN TableD
                ON TableD.dID = TableA.dID
        WHERE DATE(TableC.date)=date(now())
        """

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
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        """
        Return all items for the logged in user on a specific
        shopping list

        :param request:
        :param kwargs:
        :return:
        """
        items = Item.objects.raw(
            "select * from api_item where "
            "api_item.the_list_id=%s",
            [kwargs['list_id']]
        )
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
