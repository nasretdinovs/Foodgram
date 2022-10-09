from django.contrib.auth import get_user_model
from django.db import models
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Ingredient, IngredientAmount, Recipe, Tag

User = get_user_model()


class LiteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецептов. С меньшим количеством полей."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class SubscribeSerializer(CustomUserSerializer):
    """Сериализатор для подписки."""
    recipes = LiteRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.IntegerField(
        source='recipes.count',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = '__all__',

    def get_is_subscribed(*args):
        return True


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецептов."""
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('is_favorite', 'is_shopping_cart', )

    def get_ingredients(self, obj):
        """Получение списка ингредиентов."""
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=models.F('recipe__amount')
        )

    def get_is_favorited(self, obj):
        """Проверка на наличие рецепта в избранном."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверка на наличие рецепта в списке покупок."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.carts.filter(id=obj.id).exists()

    def create_ingredients(self, ingredients, recipe):
        """Создание количества ингредиентов."""
        objs = (IngredientAmount(
            recipe=recipe,
            ingredients=ingredient['ingredient'],
            amount=ingredient['amount']
        ) for ingredient in ingredients)
        IngredientAmount.objects.bulk_create(objs)

    def validate(self, data):
        """Проверка данных."""
        name = str(self.initial_data.get('name')).strip()
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        values_list = (tags, ingredients)

        for value in values_list:
            if not isinstance(value, list):
                raise serializers.ValidationError(
                    f'"{value}" должен быть в формате "[]"'
                )

        for tag in tags:
            if not str(tag).isdecimal():
                raise serializers.ValidationError(
                    f'{tag} должно состоять из цифр'
                )

            if not Tag.objects.filter(id=tag):
                raise serializers.ValidationError(
                    f'{tag} не существует'
                )

        valid_ingredients = []
        for ingredient_item in ingredients:
            ingredient_id = ingredient_item.get('id')
            if not str(ingredient_id).isdecimal() or str(ingredient_id) == '0':
                raise serializers.ValidationError(
                    f'Убедитесь, что значение {ingredient_id} '
                    f'является числом больше 0'
                )

            if not Ingredient.objects.filter(id=ingredient_id):
                raise serializers.ValidationError(
                    f'{ingredient_id} не существует'
                )
            ingredient = Ingredient.objects.filter(id=ingredient_id)[0]

            amount = ingredient_item.get('amount')
            if not str(amount).isdecimal() or str(amount) == '0':
                raise serializers.ValidationError(
                    f'Убедитесь, что значение {amount} '
                    f'является числом больше 0'
                )

            valid_ingredients.append(
                {'ingredient': ingredient, 'amount': amount}
            )

        data['name'] = name.capitalize()
        data['tags'] = tags
        data['ingredients'] = valid_ingredients
        data['author'] = self.context.get('request').user
        return data

    def create(self, validated_data):
        """Создание рецепта."""
        image = validated_data.pop('image')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, recipe, validated_data):
        """Обновление рецепта."""
        tags = validated_data.get('tags')
        ingredients = validated_data.get('ingredients')

        recipe.image = validated_data.get(
            'image', recipe.image)
        recipe.name = validated_data.get(
            'name', recipe.name)
        recipe.text = validated_data.get(
            'text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)

        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)

        if ingredients:
            recipe.ingredients.clear()
            self.create_ingredients(ingredients, recipe)

        recipe.save()
        return recipe
