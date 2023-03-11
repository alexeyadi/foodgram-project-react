from django.contrib.admin import register, ModelAdmin
from django.contrib.admin import display

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingList, Tag)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug',)


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'id', 'author', 'count_favorites')
    readonly_fields = ('count_in_favorites',)
    list_filter = ('author', 'name', 'tags',)

    @display(description='Количество в избранных')
    def count_favorites(self, obj):
        return obj.favorites.count()


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe',)


@register(IngredientRecipe)
class IngredientRecipe(ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)


@register(ShoppingList)
class ShoppingListAdmin(ModelAdmin):
    list_display = ('user', 'recipe',)
