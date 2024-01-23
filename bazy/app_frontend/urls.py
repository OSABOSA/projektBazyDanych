# frontend/urls.py
from django.urls import path
from .views import create_user, delete_user, create_table_and_add_entries, add_entries_to_dynamic_table
from .views import drop_table_by_name, clear_entries_by_username, get_activities_by_discipline_name
from .views import create_activity_entry, remove_activity_entry

urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('delete_user/', delete_user, name='delete_user'),
    path('create_table_and_add_entries/', create_table_and_add_entries, name='create_table_and_add_entries'),
    path('add_entries_to_dynamic_table/', add_entries_to_dynamic_table, name='add_entries_to_dynamic_table'),
    path('drop_table_by_name/', drop_table_by_name, name='drop_table_by_name'),
    path('clear_entries_by_username/', clear_entries_by_username, name='clear_entries_by_username'),
    path('get_activities_by_discipline_name/', get_activities_by_discipline_name, name='get_activities_by_discipline_name'),
    path('create_activity_entry/', create_activity_entry, name='create_activity_entry'),
    path('remove_activity_entry/', remove_activity_entry, name='remove_activity_entry'),
]
