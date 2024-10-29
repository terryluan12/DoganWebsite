from django.db import models

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)