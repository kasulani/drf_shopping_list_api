from rest_framework import viewsets
from api.serializers import ShoppingListSerializer
from api.models import ShoppingList
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status


class ShoppingLists(viewsets.ModelViewSet):
    """
    Shopping Lists CRUD endpoints
    """

    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
