from api.views import (FavoriteViewSet, IngredientsViewSet, RecipesViewSet,
                       ShoppingListViewSet, SubscriptionsViewSet, TagsViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', SubscriptionsViewSet, basename='subscription')
router.register('recipes', ShoppingListViewSet, basename='shopping_list')
router.register('recipes', FavoriteViewSet, basename='favorite')
router.register('recipes', RecipesViewSet)
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
