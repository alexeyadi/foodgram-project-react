from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)


class IngredienRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    fields = ('ingredient', 'amount',)
    min = 1
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'quantity_of_favorites',)
    list_editable = ('name', 'author')
    search_fields = ('name', 'author', 'author__first_name', 'author__email',)
    list_filter = ('tags',)
    empty_value_display = '-пусто-'
    inlines = (IngredienRecipeInline,)

    def quantity_of_favorites(self, obj):
        return obj.favorite.count()

    quantity_of_favorites.short_description = 'Количество в избранном'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    list_editable = ('name', 'slug',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    list_editable = ('name', 'measurement_unit',)
    search_fields = ('name',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount',)
    list_editable = ('ingredient', 'amount')
    search_fields = ('ingredient',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    list_editable = ('user', 'recipe',)
    list_filter = ('user',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    list_editable = ('user', 'recipe',)
    list_filter = ('user',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
