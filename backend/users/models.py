from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для пользователей."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        verbose_name='адрес электронной почты'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='уникальный юзернейм',
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='фамилия'
    )
    password = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='пароль'
    )
    subscribe = models.ManyToManyField(
        to='self',
        related_name='subscribes',
        symmetrical=False,
        verbose_name='Подписка',
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('username',)
        constraints = (
            models.CheckConstraint(
                check=models.Q(username__length__gte=3),
                name='\nusername too short\n',
            ),
        )

    def __str__(self):
        return f'{self.get_full_name()}: {self.email}'


class Subscribe(User):
    """Модель прокси для отображения подписок в админке."""
    class Meta:
        proxy = True
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
