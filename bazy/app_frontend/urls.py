# frontend/urls.py
from django.urls import path
from .views import create_user, delete_user, add_entries_to_history
from .views import drop_table_by_name, clear_entries_by_username, get_activities_by_discipline_name
from .views import create_activity_entry, remove_activity_entry, update_elo

urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('delete_user/', delete_user, name='delete_user'),
    path('add_entries_to_history/', add_entries_to_history, name='add_entries_to_history'),
    #TODO: niepotrzebne
    path('drop_table_by_name/', drop_table_by_name, name='drop_table_by_name'),

    path('clear_entries_by_username/', clear_entries_by_username, name='clear_entries_by_username'),
    path('get_activities_by_discipline_name/', get_activities_by_discipline_name, name='get_activities_by_discipline_name'),
    path('create_activity_entry/', create_activity_entry, name='create_activity_entry'),
    path('remove_activity_entry/', remove_activity_entry, name='remove_activity_entry'),
    path('update_elo/', update_elo, name='update_elo'),
]
