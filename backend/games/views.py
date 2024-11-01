from django.shortcuts import render

from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework import generics, status, permissions
from rest_framework.views import Response, APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Game
from .serializers import GameSerializer
from .permissions import IsAdminDelete, IsInGameDelete

class GameDetailView(generics.RetrieveDestroyAPIView, generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'game_name'
    permission_classes = [IsAdminDelete]

    def perform_create(self, serializer):
        game_name = self.kwargs.get("game_name")
        if Game.objects.filter(game_name=game_name).exists():
            raise ValidationError("Game already exists.")
        user = getOrCreateUser(self.request)
        game = serializer.save(game_name=self.kwargs.get("game_name"), admin=user)
        addUser(game, user, "Game created and user added to game.")

class GamePlayerView(APIView):

    def get_object(self):
        game_name = self.kwargs.get('game_name')
        return get_object_or_404(Game, game_name=game_name)

    def post(self, request, *args, **kwargs):
        game = self.get_object()
        user = getOrCreateUser(request)
        return addUser(game, user)
        
    def delete(self, request, *args, **kwargs):
        game = self.get_object()
        return deleteUser(game, request.user)

class RemovePlayerView(APIView):
    permission_classes = [IsAdminDelete]

    def delete(self, request, *args, **kwargs):
        game = get_object_or_404(Game, game_name=self.kwargs.get('game_name'))
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        self.check_object_permissions(request, game)
        return deleteUser(game, user)

class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAdminUser]

### Helper functions

def deleteUser(game, user):
    if not user.game or user not in game.users.all():
        raise ValidationError("User not in game.")
    user.game = None
    user.save()
    if game.users.count() == 0:
        game.delete()
        return Response({
            'message': 'Game deleted.'
        }, status=status.HTTP_204_NO_CONTENT)
    if game.admin == user:
        game.admin = game.users.first()
        game.save()
    users = UserSerializer(game.users, many=True).data
    admin = UserSerializer(game.admin).data
    return Response({
        'game_name': game.game_name,
        'users': users,
        'admin': admin,
        'message': 'User removed from game.'
    }, status=status.HTTP_200_OK)

def addUser(game, user, message="User added to game."):
    if user.game:
        raise ValidationError("User already in a game.")
    else:
        game.users.add(user)
        game.save()
        users = UserSerializer(game.users, many=True).data
        admin = UserSerializer(game.admin).data
        return Response({
            'game_name': game.game_name,
            'users': users,
            'admin': admin,
            'message': message
        }, status=status.HTTP_201_CREATED)
def getOrCreateUser(request):
    if not request.user.is_authenticated:
        user = User.objects.create(temporary=True)
        user.save()
        login(request, user)
    else:
        user = request.user
    return user