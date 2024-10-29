import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.base_session import AbstractBaseSession
from django.conf import settings
from .utils import generateName
from games.models import Game

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    username = models.CharField(unique=True, default=generateName, max_length=100, blank=True)
    game = models.ForeignKey(Game, related_name="users", null=True, on_delete=models.SET_NULL)
    time_created = models.DateTimeField(default=timezone.now)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    abandons = models.IntegerField(default=0)
    temporary = models.BooleanField(default = False)
    
    # Registered User Specific Fields
    email = models.EmailField('email address', unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    
    # Django User Fields
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    
    def save(self, *args, **kwargs):
        if not self.email:
            self.temporary = True
        else:
            self.temporary = False
        super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()
        if not self.temporary:
            if not self.username:
                self.username = generateName()
            if not self.email:
                raise ValidationError('Email is required for non-temporary users.')
            if not self.password:
                raise ValidationError('Password is required for non-temporary users.')
        self.email = self.__class__.objects.normalize_email(self.email)