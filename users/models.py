from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(
        upload_to='users/avatars',
        verbose_name='Avatar',
        blank=True, null=True,
        help_text='Загрузите аватар'
    )
    phone = models.CharField(
        max_length=35,
        verbose_name='Телефон',
        blank=True,
        null=True,
        help_text='Введите номер телефона'
    )
    country = models.CharField(
        max_length=50,
        verbose_name='Страна',
        blank=True, null=True,
        help_text='Введите страну'
    )

    token = models.CharField(max_length=100, verbose_name='Токен', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
                    ('deactivate_user', 'Can deactivate user'),
                    ('view_all_users', 'Can view all users'),
                ]

    def __str__(self):
        return self.email
