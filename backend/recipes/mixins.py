from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)


class AddRemoveMixin:
    """Добавление доп. функций во вьюсет."""
    extra_serializer = None

    def add_remove_obj(self, obj_id, our_field):
        """Добавляет или удаляет зависимость many-to-many."""
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)

        fields = {
            'subscribe': user.subscribe,
            'favorite': user.favorites,
            'shopping_cart': user.carts,
        }
        our_field = fields[our_field]

        obj = get_object_or_404(self.queryset, id=obj_id)
        serializer = self.extra_serializer(
            obj, context={'request': self.request}
        )
        obj_exist = our_field.filter(id=obj_id).exists()

        if (self.request.method in ('GET', 'POST',)) and not obj_exist:
            our_field.add(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if (self.request.method in ('DELETE',)) and obj_exist:
            our_field.remove(obj)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)
