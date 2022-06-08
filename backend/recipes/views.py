from datetime import datetime as dt
from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http.response import HttpResponse

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from .mixins import AddRemoveMixin
from .paginators import CustomPageNumberPagination
from .permissions import AdminOrReadOnly, AuthorOrReadOnly
from .serializers import (IngredientSerializer, LiteRecipeSerializer,
                          RecipeSerializer, TagSerializer)

User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)

    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = self.queryset
        if name:
            name = name.lower()
            stw_queryset = list(queryset.filter(name__startswith=name))
            cnt_queryset = queryset.filter(name__contains=name)
            stw_queryset.extend(
                [i for i in cnt_queryset if i not in stw_queryset]
            )
            queryset = stw_queryset
        return queryset


class RecipeViewSet(ModelViewSet, AddRemoveMixin):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    extra_serializer = LiteRecipeSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset

        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()

        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)

        # Для авторизованных пользователей:
        user = self.request.user
        if user.is_anonymous:
            return queryset

        is_in_shopping = self.request.query_params.get('is_in_shopping_cart')
        if is_in_shopping in ('1', 'true',):
            queryset = queryset.filter(cart=user.id)
        elif is_in_shopping in ('0', 'false',):
            queryset = queryset.exclude(cart=user.id)

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited in ('1', 'true',):
            queryset = queryset.filter(favorite=user.id)
        if is_favorited in ('0', 'false',):
            queryset = queryset.exclude(favorite=user.id)

        return queryset

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        return self.add_remove_obj(pk, 'favorite')

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def shopping_cart(self, request, pk):
        return self.add_remove_obj(pk, 'shopping_cart')

    @action(methods=['GET'], detail=False)
    def download_shopping_cart(self, request):
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
