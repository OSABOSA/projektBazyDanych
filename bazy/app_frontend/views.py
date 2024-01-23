from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.middleware.csrf import get_token
from .models import User, Activity, create_dynamic_model, Discipline

# views.py
from django.http import JsonResponse
from .models import create_dynamic_model
from django.apps import apps
from django.db import connection
from django.db.utils import ProgrammingError
from django.apps.config import AppConfig
from django.db import models


def user_id_to_username(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user.name
    except User.DoesNotExist:
        return None


def username_to_user_id(username):
    try:
        user = User.objects.get(name=username)
        return user.id
    except User.DoesNotExist:
        return None


def discipline_id_to_name(discipline_id):
    try:
        discipline = Discipline.objects.get(id=discipline_id)
        return discipline.name
    except Discipline.DoesNotExist:
        return None


def name_to_discipline_id(name):
    try:
        discipline = Discipline.objects.get(name=name)
        return discipline.id
    except Discipline.DoesNotExist:
        return None


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        User.objects.create(name=name, email=email, password=password, phone=phone)
        return JsonResponse({'message': 'User created successfully'})
    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def delete_user(request):
    username = request.POST.get('name', '')

    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)

    try:
        # Try to get the user by username and delete if found
        user = User.objects.get(name=username)
        user.delete()

        return JsonResponse({'message': f'User "{username}" deleted successfully'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': f'User "{username}" not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error deleting user: {str(e)}'}, status=500)


@csrf_exempt
def create_table_and_add_entries(request):
    table_name = request.POST.get('table_name', '')

    if not table_name:
        return JsonResponse({'error': 'Table name is required'}, status=400)

    # Ensure the model is not already registered
    if not apps.is_installed('app_frontend'):
        apps.app_configs['app_frontend'] = AppConfig('app_frontend', 'app_frontend')

    model_class_name = f'DynamicModel_{table_name}'

    if model_class_name not in globals():
        # Create the dynamic model
        class DynamicModel(models.Model):
            opponent_id = models.IntegerField()
            discipline = models.CharField(max_length=255)
            result = models.CharField(max_length=255)
            has_ended = models.BooleanField()

            class Meta:
                db_table = f'{table_name}'

        globals()[model_class_name] = DynamicModel

        # Create the table
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(DynamicModel)

        return JsonResponse({'message': 'Table created successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Table already exists'}, status=400)


@csrf_exempt
def add_entries_to_dynamic_table(request):
    try:
        username = request.POST.get('username', '')
        opponent_id = username_to_user_id(request.POST.get('opponent', ''))
        discipline = request.POST.get('sport', '')
        result = request.POST.get('result', '')
        has_ended = True
        dynamic_model = globals()[f'DynamicModel_{username}']

        # Validate that all required fields are present
        if not opponent_id or not discipline or not result or has_ended is None:
            return JsonResponse({'error': 'All fields are required for the entry'}, status=400)

        # Create entries in the table using data from the POST request
        dynamic_model.objects.create(
            opponent_id=opponent_id,
            discipline=discipline,
            result=result,
            has_ended=bool(int(has_ended))  # Convert has_ended to a boolean
        )

        return JsonResponse({'message': f'Entries added to {username} successfully'}, status=200)
    except KeyError:
        return JsonResponse({'error': f'DynamicModel_{username} not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error adding entries: {str(e)}'}, status=500)


@csrf_exempt
def drop_table_by_name(request):
    table_name = request.POST.get('name', '')

    if not table_name:
        return JsonResponse({'error': 'Username is required'}, status=400)

    try:
        # Drop the table
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(table_name)

        return JsonResponse({'message': f'Table "{table_name}" dropped successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': f'Error dropping table: {str(e)}'}, status=500)


@csrf_exempt
def clear_entries_by_username(request):
    username = request.POST.get('name', '')

    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)

    try:
        # Retrieve the user_id from the User table
        user = User.objects.get(name=username)
        user_id = user.id

        # Clear entries from the OtherTable based on user_id
        Activity.objects.filter(user_id=user_id).delete()

        return JsonResponse({'message': f'Entries for user "{username}" cleared successfully'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': f'User "{username}" not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error clearing entries: {str(e)}'}, status=500)


@csrf_exempt
def get_activities_by_discipline_name(request):
    name = request.GET.get('sport', '')
    print(name)

    if not name:
        return JsonResponse({'error': 'Discipline name is required'}, status=400)

    try:
        # Retrieve the discipline_id from the DisciplineTable
        discipline = Discipline.objects.get(name=name)
        discipline_id = discipline.discipline_id

        # Get all entries from the Activity model where discipline_id matches
        activities = Activity.objects.filter(discipline_id=discipline_id)

        # Serialize the activities and return them as JSON
        serialized_activities = [{'username': user_id_to_username(activity.user_id), 'elo': activity.elo} for activity in activities]

        return JsonResponse({'activities': serialized_activities}, status=200)
    except Discipline.DoesNotExist:
        return JsonResponse({'error': f'Discipline "{discipline_name}" not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error retrieving activities: {str(e)}'}, status=500)


@csrf_exempt
def create_activity_entry(request):
    # Assuming you are receiving these values through a POST request
    user_id = username_to_user_id(request.POST.get('username', ''))
    discipline_id = name_to_discipline_id(request.POST.get('sport', ''))  # Convert the sport name to discipline_id
    elo = request.POST.get('elo', '')

    # Check if any required field is missing
    if not user_id or not discipline_id or not elo:
        return JsonResponse({'error': 'user_id, discipline_id, and elo are required fields'}, status=400)

    try:
        # Create a new entry in the Activity model
        activity = Activity.objects.create(user_id=user_id, discipline_id=discipline_id, elo=elo)

        return JsonResponse({'message': 'Activity entry created successfully', 'activity_id': activity.id}, status=200)
    except Exception as e:
        return JsonResponse({'error': f'Error creating activity entry: {str(e)}'}, status=500)


@csrf_exempt
def remove_activity_entry(request):
    user_id = username_to_user_id(request.POST.get('username', ''))
    discipline_id = name_to_discipline_id(request.POST.get('sport', ''))

    if not user_id or not discipline_id:
        return JsonResponse({'error': 'user_id and discipline_id are required'}, status=400)

    try:
        # Try to get the activity by user_id and discipline_id and delete if found
        activity = Activity.objects.get(user_id=user_id, discipline_id=discipline_id)
        activity.delete()

        return JsonResponse({'message': f'Activity entry for user_id={user_id} and discipline_id={discipline_id} deleted successfully'}, status=200)
    except Activity.DoesNotExist:
        return JsonResponse({'error': f'Activity entry for user_id={user_id} and discipline_id={discipline_id} not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error deleting activity entry: {str(e)}'}, status=500)
