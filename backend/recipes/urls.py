from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'recipes'

router_v1 = routers.DefaultRouter()
router_v1.register('tags', TagViewSet, 'tags')
router_v1.register('ingredients', IngredientViewSet, 'ingredients')
router_v1.register('recipes', RecipeViewSet, 'recipes')
router_v1.register('users', UserViewSet, 'users')

urlpatterns = (
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
)
