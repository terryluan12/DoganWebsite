from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import Http404
from rest_framework import generics, status
from rest_framework.views import Response, APIView

from .models import User
from .serializers import UserSerializer, PublicUserSerializer
from .utils import get_client_ip, generateName


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        if user.is_anonymous:
            raise Http404("User not found.")
        return user

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer

class SessionView(APIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    def post(self, request):
        if "username" not in request.data and "password" not in request.data:
            user = User.objects.create(temporary=True)
            user.save()
        else:
            user = authenticate(request, username=request.data['username'], password=request.data['password'])
        
        login(request, user)
            
        return Response({
            'username': user.username,
            'message': 'User logged in.'
        }, status=status.HTTP_200_OK)
        
    def delete(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)