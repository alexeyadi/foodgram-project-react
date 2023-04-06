from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, CharField, EmailField, ForeignKey,
                              Model, UniqueConstraint)


class User(AbstractUser):
    '''Custom user model.'''
    email = EmailField(
        'Email',
        max_length=254,
        unique=True,
    )

    first_name = CharField(
        'Имя',
        max_length=150,
    )

    last_name = CharField(
        'Фамилия',
        max_length=150,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(Model):
    '''Subscription to author.'''
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписался на {self.author.username}'
