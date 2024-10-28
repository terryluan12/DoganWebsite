from rest_framework import serializers

from accounts.serializers import UserSerializer
from games.models import Game


class GameSerializer(serializers.ModelSerializer):
    registered_users = UserSerializer(many=True)
    class Meta:
        model = Game
        fields = ['session_id', 'session_name', 'registered_users']
        depth = 2
    def create(self, validated_data):
        users_data = validated_data.pop('users')
        users = [User.objects.create(**user_data) for user_data in users_data]
        game = Game.objects.create(users=users, **profile_data)
        return game
