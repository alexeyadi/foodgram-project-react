import base64

from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        ImageField, IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField, ValidationError)
from rest_framework.validators import UniqueTogetherValidator
from users.models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    '''Serializer to work with custom User creation model.'''
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class CustomUserSerializer(UserSerializer):
    '''Serializer to work with custom User model.'''
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            user = get_object_or_404(
                User, username=self.context['request'].user)
            return user.follower.filter(author=obj.id).exists()
        return False

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class IngredientSerializer(ModelSerializer):
    '''Serializer to work with Ingredient model.'''
    class Meta:
        model = Ingredient
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Ingredient.objects.all(),
                fields=('name', 'measurement_unit'),
                message=('Ингредиент уже добавлен.')
            )
        ]


class TagSerializer(ModelSerializer):
    '''Serializer to work with Tag model.'''
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientRecipeSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = CharField(source='ingredient.name', read_only=True)
    measurement_unit = CharField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        extra_kwargs = {
            'amount': {
                'min_value': None,
            },
        }


class Base64ImageField(ImageField):
    '''Class for images'''
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(ModelSerializer):
    '''Serializer for recipe's list'''
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(many=True,
                                             source='recipe_ingredients')
    author = CustomUserSerializer(read_only=True,
                                  default=CurrentUserDefault())
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            user = get_object_or_404(
                User, username=self.context['request'].user)
            return user.favorite.filter(recipe=obj.id).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            user = get_object_or_404(
                User, username=self.context['request'].user)
            return user.cart.filter(recipe=obj.id).exists()
        return False

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')


class RecipeCreateSerializer(RecipeSerializer):
    '''Serializer for create recipe.'''
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    @staticmethod
    def _save_ingredients(recipe, ingredients):
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = ingredient['ingredient']['id']
            current_amount = ingredient['amount']
            ingredients_list.append(
                IngredientRecipe(
                    recipe=recipe,
                    ingredient=current_ingredient,
                    amount=current_amount))
        IngredientRecipe.objects.bulk_create(ingredients_list)

    def validate(self, data):
        if data['cooking_time'] <= 0:
            raise ValidationError('Время приготовления не может '
                                  'быть менее минуты.')

        ingredients_list = []
        for ingredient in data['recipe_ingredients']:
            if ingredient['amount'] <= 0:
                raise ValidationError('Количество не может'
                                      ' быть меньше 1.')
            ingredients_list.append(ingredient['ingredient']['id'])

        if len(ingredients_list) > len(set(ingredients_list)):
            raise ValidationError('Ингредиенты не должны'
                                  ' повторяться.')
        return data

    @transaction.atomic
    def create(self, validated_data):
        author = self.context['request'].user
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.add(*tags)
        self._save_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)
        instance.ingredients.clear()
        recipe = instance
        self._save_ingredients(recipe, ingredients)
        instance.save()
        return instance

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        extra_kwargs = {
            'cooking_time': {
                'min_value': 1,
            },
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('author', 'name'),
                message='Название должно быть уникальным.'
            )
        ]


class ShortRecipeSerializer(RecipeSerializer):
    '''Serializer to work with ShortRecipe.'''

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class SubscriptionSerializer(CustomUserSerializer):
    '''Serializer to work with Subscription model.'''
    recipes = ShortRecipeSerializer(read_only=True, many=True)
    recipes_count = IntegerField(source='recipes.count', read_only=True)

    def validate(self, data):
        user = self.context['request'].user
        author = self.instance
        if user == author:
            raise ValidationError('Нельзя подписаться на самого себя!')
        return data

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
