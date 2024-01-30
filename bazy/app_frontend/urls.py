# frontend/urls.py
from django.urls import path
from .views import get_user, create_user, get_disciplines, get_activities_by_discipline_name \
    , add_activity, remove_activity, request_match, get_games, \
    reject_game, avengers, accept_game


urlpatterns = [
    path('get_user/', get_user),
    path('get_disciplines/', get_disciplines),
    path('create_user/', create_user),
    path('get_activities/', get_activities_by_discipline_name),
    path('add_activity/', add_activity),
    path('remove_activity/', remove_activity),
    path('request_match/', request_match),
    path('get_games/', get_games),
    path('reject_game/', reject_game),
    path('accept_game/', accept_game),
    path('avengers/', avengers),
]
