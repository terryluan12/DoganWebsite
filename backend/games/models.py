from django.db import models

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=30, unique=True)
    admin = models.OneToOneField('accounts.User', on_delete=models.CASCADE, blank=True, related_name='admin_game')