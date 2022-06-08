from django.contrib.auth import get_user_model

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from recipes.mixins import AddRemoveMixin
from recipes.paginators import CustomPageNumberPagination
from recipes.serializers import SubscribeSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet, AddRemoveMixin):
    pagination_class = CustomPageNumberPagination
    extra_serializer = SubscribeSerializer

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def subscribe(self, request, id):
        return self.add_remove_obj(id, 'subscribe')

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        authors = user.subscribe.all()
        pages = self.paginate_queryset(authors)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
