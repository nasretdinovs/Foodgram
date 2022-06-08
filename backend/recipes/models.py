from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Length

models.CharField.register_lookup(Length)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='название',
    )
    color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        default='#FFFF00',
        verbose_name='цвет в HEX',
    )
    slug = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='уникальный слаг',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ('name', )
        constraints = (
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='tag_name_length_gt_0',
            ),
            models.CheckConstraint(
                check=models.Q(color__length__gt=0),
                name='tag_color_length_gt_0',
            ),
            models.CheckConstraint(
                check=models.Q(slug__length__gt=0),
                name='tag_slug_length_gt_0',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name} (цвет: {self.color})'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='ингредиент',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='единица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ('name', )
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='ingredient_unique'
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='ingredient_name_length_gt_0',
            ),
            models.CheckConstraint(
                check=models.Q(measurement_unit__length__gt=0),
                name='ingredient_measurement_unit_length_gt_0',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='тег',
        related_name='recipes',
    )
    author = models.ForeignKey(
        User,
        verbose_name='автор рецепта',
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='список ингредиентов',
        related_name='recipes',
        through='recipes.IngredientAmount',
    )
    favorite = models.ManyToManyField(
        User,
        verbose_name='находится ли в избранном',
        related_name='favorites',
    )
    cart = models.ManyToManyField(
        User,
        verbose_name='находится ли в корзине',
        related_name='carts',
    )
    name = models.CharField(
        verbose_name='название',
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='ссылка на картинку на сайте',
        upload_to='recipe/',
    )
    text = models.TextField(
        verbose_name='описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время приготовления (в минутах)',
        default=0,
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ('-pub_date', )
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='recipe_unique'
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='recipe_name_length_gt_0',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name}. Автор рецепта: {self.author.username}'


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='из рецепта',
        related_name='ingredient',
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name='ингредиенты',
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество',
        default=0,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'количество ингредиента'
        verbose_name_plural = 'количество ингредиентов'
        ordering = ('recipe', )
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredients', ),
                name='ingredient_amount_unique',
            ),
        )

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredients}'
