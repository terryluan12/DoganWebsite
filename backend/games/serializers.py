from rest_framework import serializers

from accounts.serializers import UserSerializer
from games.models import Game


class GameSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, required=False)
    class Meta:
        model = Game
        fields = ['game_id', 'users']
        read_only_fields = ['game_id']
        depth = 2
    def create(self, validated_data):
        users_data = validated_data.pop('users')
        game = Game.objects.create(**validated_data)
        for user_data in users_data:
            game.users.add(user_data)
        return game