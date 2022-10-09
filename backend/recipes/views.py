from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http.response import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from .filters import IngredientFilter, TagAuthorFilter
from .mixins import AddRemoveMixin
from .paginators import CustomPageNumberPagination
from .permissions import AdminOrReadOnly, AuthorOrReadOnly
from .serializers import (IngredientSerializer, LiteRecipeSerializer,
                          RecipeSerializer, TagSerializer)

User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    """Изменение и создание тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Изменение и создание ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet, AddRemoveMixin):
    """Изменение и создание рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    extra_serializer = LiteRecipeSerializer
    pagination_class = CustomPageNumberPagination
    filter_class = TagAuthorFilter
    permission_classes = (AuthorOrReadOnly,)

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        """Добавление или удаление рецепта из избранного."""
        return self.add_remove_obj(pk, 'favorite')

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def shopping_cart(self, request, pk):
        """Добавление или удаление рецепта из списка покупок."""
        return self.add_remove_obj(pk, 'shopping_cart')

    @action(methods=['GET'], detail=False)
    def download_shopping_cart(self, request):
        """Создание и скачивание списка покупок в формате *.TXT"""
        user = self.request.user
        if not user.carts.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        ingredients = IngredientAmount.objects.filter(
            recipe__in=(user.carts.values('id'))
        ).values(
            ingredient=F('ingredients__name'),
            measure=F('ingredients__measurement_unit')
        ).annotate(amount=Sum('amount'))

        filename = f'{user.username}_shopping_list.txt'
        shopping_list = (
            f'Список покупок от '
            f'{dt.now().strftime("%d.%m.%Y, %H:%M")}'
        )
        for ing in ingredients:
            shopping_list += (
                f'\n- {ing["ingredient"]}: {ing["amount"]} {ing["measure"]}'
            )

        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
