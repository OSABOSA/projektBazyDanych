# frontend/urls.py
from django.urls import path
from .views import get_users, add_user, get_csrf_token

urlpatterns = [
    path('get_users/', get_users, name='get_users'),
    path('add_user/', add_user, name='add_user'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
]
