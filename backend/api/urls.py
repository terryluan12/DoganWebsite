"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path
from accounts import views as accounts_views
from games import views as games_views
from messages import views as messages_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('game/<game_name>', games_views.GameDetailView.as_view()),
    path('game/<game_name>/player', games_views.GamePlayerView.as_view()),
    path('game/<game_name>/player/<username>', games_views.RemovePlayerView.as_view()),
    path('games', games_views.GameListView.as_view()),
    
    path('user', accounts_views.UserCreateView.as_view()),
    path('user/me', accounts_views.CurrentUserView.as_view()),
    path('user/session', accounts_views.SessionView.as_view()),
    path('user/<username>', accounts_views.UserDetailView.as_view()),
    path('users', accounts_views.UserListView.as_view()),
]
