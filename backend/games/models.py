from django.db import models

class Game(models.Model):
    session_id = models.IntegerField(primary_key=True)
    session_name = models.CharField(max_length=100)