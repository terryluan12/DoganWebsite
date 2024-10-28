from django.shortcuts import render

from rest_framework import generics

from .models import Game
from .serializers import GameSerializer

class GameDetailView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
