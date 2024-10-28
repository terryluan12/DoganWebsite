import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from games.models import Game

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField('email address', unique=True)
    ip_address = models.GenericIPAddressField()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'ip_address']
    game_id = models.ForeignKey(Game, related_name="registered_users", blank=True, null=True, on_delete=models.SET_NULL)