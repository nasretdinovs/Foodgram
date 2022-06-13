from django.contrib import admin

from .models import Ingredient, IngredientAmount, Recipe, Tag

admin.site.register(IngredientAmount)


class IngredientInline(admin.TabularInline):
    model = IngredientAmount
    extra = 2


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )
    empty_value_display = '-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'color',)
    ordering = ('name',)
    empty_value_display = '-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'get_favor_count'
    )
    inlines = (IngredientInline,)
    filter_horizontal = ('tags',)
    search_fields = ('name', 'author', 'tags',)
    list_filter = ('author', 'name', 'tags')
    ordering = ('author', 'pub_date',)
    empty_value_display = '-'

    def get_favor_count(self, obj):
        return obj.favorite.count()
    get_favor_count.short_description = 'в избранном'
