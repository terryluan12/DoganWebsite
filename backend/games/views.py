from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import Response

from .models import Game
from .serializers import GameSerializer

class GameDetailView(generics.RetrieveDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameCreateView(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])

class AddPlayerView(generics.UpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.users.add(request.user)
        instance.save()
        return Response({
            'game_id': instance.game_id,
            'message': 'User added to game.'
        }, status=status.HTTP_200_OK)

class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
