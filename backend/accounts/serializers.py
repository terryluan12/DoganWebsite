from rest_framework import serializers
from .models import User
from games.models import Game

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password', 'email']
        read_only_fields = ['user_id', 'game', 'wins', 'losses', 'time_created']

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'wins', 'losses']