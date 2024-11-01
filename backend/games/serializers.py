from rest_framework import serializers

from accounts.serializers import UserSerializer
from games.models import Game


class GameSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, required=False)
    admin = UserSerializer(required=False)
    class Meta:
        model = Game
        fields = ['users', 'game_name', 'admin']
        read_only_fields = ['game_id', 'game_name']
        depth = 2