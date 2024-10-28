from django.shortcuts import render
from rest_framework import generics

from .models import User
from .serializers import UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer