from django.core.validators import MinValueValidator, RegexValidator
from django.db.models import (Model, CharField, SlugField, ForeignKey, CASCADE,
                              ImageField, TextField, ManyToManyField,
                              IntegerField, DateTimeField, UniqueConstraint)
from users.models import User


class Tag(Model):
    '''Model for recipes tags.'''
    name = CharField(
        'Название',
        max_length=200
    )
    color = CharField(
        'Цвет в HEX',
        max_length=7,
        null=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message='Введите HEX-код цвета.'
            )
        ]

    )
    slug = SlugField(
        'Слаг',
        max_length=200,
        unique=True,
        null=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(Model):
    '''Model of ingredient.'''
    name = CharField(
        'Название',
        max_length=200
    )
    measurement_unit = CharField(
        'Единица измерения',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(Model):
    '''Model of recipe.'''
    author = ForeignKey(
        User, on_delete=CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )

    name = CharField(
        max_length=200,
        verbose_name='Название'
    )

    image = ImageField(
        upload_to='recipes/',
        verbose_name='Картинка'
    )

    text = TextField(
        verbose_name='Описание'
    )

    ingredients = ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        related_name='recipes',
        blank=False
    )

    tags = ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )

    cooking_time = IntegerField(
        validators=[
            MinValueValidator(1, 'Время приготовления не менее минуты.'),
        ],
        verbose_name='Время приготовления в минутах'
    )

    created = DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ['-created']
        constraints = [
            UniqueConstraint(
                fields=['author', 'name'],
                name='unique_author_name')
        ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorite(Model):
    '''Model of favorite recipes.'''
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorite_user',
        verbose_name='Подписчик'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorite_recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class IngredientRecipe(Model):
    '''Model for link Ingredient and Recipe'''
    recipe = ForeignKey(Recipe,
                        on_delete=CASCADE,
                        related_name='recipe_ingredients',
                        verbose_name='Рецепт')
    ingredient = ForeignKey(Ingredient,
                            on_delete=CASCADE,
                            related_name='recipe_ingredients',
                            verbose_name='Ингредиент')
    amount = IntegerField(
        validators=[
            MinValueValidator(1, 'Количество не менее 1.'),
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.recipe.name}: {self.ingredient.name} - {self.amount}'


class ShoppingList(Model):
    '''Model for shopping list'''
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='shopping_user',
        verbose_name='Пользователь',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='shopping_recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_list')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
