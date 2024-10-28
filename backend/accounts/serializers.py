from rest_framework import serializers
from .models import User
from games.models import Game

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'ip_address']