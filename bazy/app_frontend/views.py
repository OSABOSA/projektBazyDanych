from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.middleware.csrf import get_token
from .models import User, Activity, Discipline, History, Ongoing, Requested
from django.http import JsonResponse
from django.apps import apps
from django.db import connection
from django.db.utils import ProgrammingError
from django.apps.config import AppConfig
from django.db import models


@csrf_exempt
def get_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.get(username=username, password=password)
            return JsonResponse({'user_id': user.user_id, 'username': user.username})
        except User.DoesNotExist:
            return JsonResponse({'error': f'Wrong username or password'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error getting user: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def get_disciplines(request):
    if request.method == 'GET':
        try:
            disciplines = Discipline.objects.all()
            return JsonResponse({'disciplines': [discipline.name for discipline in disciplines]})
        except Exception as e:
            return JsonResponse({'error': f'Error getting disciplines: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'})


def user_id_to_username(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        return user.username
    except User.DoesNotExist:
        return None


def username_to_user_id(username):
    try:
        user = User.objects.get(username=username)
        return user.user_id
    except User.DoesNotExist:
        return None


def discipline_id_to_name(discipline_id):
    try:
        discipline = Discipline.objects.get(discipline_id=discipline_id)
        return discipline.name
    except Discipline.DoesNotExist:
        return None


def name_to_discipline_id(name):
    try:
        discipline = Discipline.objects.get(name=name)
        return discipline.discipline_id
    except Discipline.DoesNotExist:
        return None


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        User.objects.create(username=username, email=email, password=password, phone=phone)
        return JsonResponse({'message': 'User created successfully'})
    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def request_match(request):
    if request.method == 'POST':
        sender_id = request.POST.get('sender_id')
        discipline_id = name_to_discipline_id(request.POST.get('discipline', ''))
        sender = Activity.objects.get(user_id=sender_id, discipline_id=discipline_id)
        receiver_id = username_to_user_id(request.POST.get('receiver', ''))
        receiver = User.objects.get(user_id=receiver_id)
        try:
            print(sender, receiver)
            Requested.objects.create(activity=sender, receiver_id=receiver_id)
            return JsonResponse({'message': 'Match requested successfully'})
        except Exception as e:
            return JsonResponse({'error': f'Error requesting match: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def get_games(response):
    if response.method == 'POST':
        user_id = response.POST.get('user_id')
        try:
            history = History.objects.filter(user_id=user_id)
            h = [{'username': user_id_to_username(game.user_id), 'discipline': discipline_id_to_name(game.discipline_id), 'opponent': user_id_to_username(game.opponent_id)}for game in history]
            history_op = History.objects.filter(opponent_id=user_id)
            h += [{'username': user_id_to_username(game.opponent_id), 'discipline': discipline_id_to_name(game.discipline_id), 'opponent': user_id_to_username(game.user_id)}for game in history_op]
            ongoing = Ongoing.objects.filter(user_id=user_id)
            o = [{'username': user_id_to_username(game.user_id), 'discipline': discipline_id_to_name(game.discipline_id), 'opponent': user_id_to_username(game.opponent_id)}for game in ongoing]
            ongoing_op = Ongoing.objects.filter(opponent_id=user_id)
            o += [{'username': user_id_to_username(game.opponent_id), 'discipline': discipline_id_to_name(game.discipline_id), 'opponent': user_id_to_username(game.user_id)}for game in ongoing_op]
            requested = Requested.objects.filter(receiver_id=user_id)
            r = [{'username': user_id_to_username(game.activity.user_id), 'discipline': discipline_id_to_name(game.activity.discipline_id), 'elo': game.activity.elo}for game in requested]
            return JsonResponse({'history': h,
                                 'ongoing': o,
                                'requested': r})
        except Exception as e:
            return JsonResponse({'error': f'Error getting games: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def reject_game(response):
    if response.method == 'POST':
        try:
            u = username_to_user_id(response.POST.get('receiver'))
            d = name_to_discipline_id(response.POST.get('discipline'))
            s = response.POST.get('sender_id')
            print(u, d)
            a = Activity.objects.get(user_id=u, discipline_id=d)
            r = Requested.objects.get(activity_id=a, receiver_id=s)
            r.delete()
            return JsonResponse({'message': 'Request deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': f'Error rejecting game: {str(e)}'}, status=500)

@csrf_exempt
def accept_game(response):
    if response.method == 'POST':
        try:
            u = username_to_user_id(response.POST.get('receiver'))
            d = name_to_discipline_id(response.POST.get('discipline'))
            s = response.POST.get('sender_id')
            print(u, d)
            o = Ongoing.objects.create(user_id=u, opponent_id=s, discipline_id=d)
            a = Activity.objects.get(user_id=u, discipline_id=d)
            r = Requested.objects.get(activity_id=a, receiver_id=s)
            r.delete()
            return JsonResponse({'message': 'Request deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': f'Error rejecting game: {str(e)}'}, status=500)


@csrf_exempt
def avengers(response):
    if response.method == 'POST':
        try:
            u = username_to_user_id(response.POST.get('receiver'))
            d = name_to_discipline_id(response.POST.get('discipline'))
            s = response.POST.get('sender_id')
            h = History.objects.create(user_id=u, opponent_id=s, discipline_id=d, result=1)
            print(u, d, 's', s)
            o = Ongoing.objects.get(user_id=u, discipline_id=d, opponent_id=s)
            o.delete()
            return JsonResponse({'message': 'Request moved to history successfully'})
        except Exception as e:
            return JsonResponse({'error': f'Error rejecting game: {str(e)}'}, status=500)

#
# @csrf_exempt
# def delete_user(request):
#     username = request.POST.get('name', '')
#
#     if not username:
#         return JsonResponse({'error': 'Username is required'}, status=400)
#
#     try:
#         # Try to get the user by username and delete if found
#         user = User.objects.get(name=username)
#         user.delete()
#
#         return JsonResponse({'message': f'User "{username}" deleted successfully'}, status=200)
#     except User.DoesNotExist:
#         return JsonResponse({'error': f'User "{username}" not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'error': f'Error deleting user: {str(e)}'}, status=500)
#
#
# @csrf_exempt
# def add_entries_to_history(request):
#     try:
#         username = request.POST.get('username', '')
#         user_id = username_to_user_id(username)
#         opponent_id = username_to_user_id(request.POST.get('opponent', ''))
#         discipline = request.POST.get('sport', '')
#         result = request.POST.get('result', '')
#         has_ended = True
#
#         # Validate that all required fields are present
#         if not user_id or not opponent_id or not discipline or not result or has_ended is None:
#             return JsonResponse({'error': 'All fields are required for the entry'}, status=400)
#
#         # Create entries in the table using data from the POST request
#         GameHistory.objects.create(
#             user_id=user_id,
#             opponent_id=opponent_id,
#             discipline=discipline,
#             result=result,
#             has_ended=bool(int(has_ended))  # Convert has_ended to a boolean
#         )
#
#         return JsonResponse({'message': f'Entries added to {username} successfully'}, status=200)
#     except KeyError:
#         return JsonResponse({'error': f'DynamicModel_{username} not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'error': f'Error adding entries: {str(e)}'}, status=500)
#
#
# @csrf_exempt
# def update_elo(request):
#     try:
#         user_id = username_to_user_id(request.POST.get('username', ''))
#         discipline_id = name_to_discipline_id(request.POST.get('sport', ''))
#         new_elo = request.POST.get('elo', '')
#         result = request.POST.get('result', '')
#         # Get the activity record based on user_id and discipline_id
#         activity = Activity.objects.get(user_id=user_id, discipline_id=discipline_id)
#
#         # Update the elo field
#         activity.elo = new_elo
#         activity.save()
#
#         return {'message': f'Elo updated successfully for user {user_id} in discipline {discipline_id}'}
#     except Activity.DoesNotExist:
#         return {'error': f'Activity not found for user {user_id} in discipline {discipline_id}'}
#     except Exception as e:
#         return {'error': f'Error updating elo: {str(e)}'}
#
#
#
# @csrf_exempt
# def drop_table_by_name(request):
#     table_name = request.POST.get('name', '')
#
#     if not table_name:
#         return JsonResponse({'error': 'Username is required'}, status=400)
#
#     try:
#         # Drop the table
#         with connection.schema_editor() as schema_editor:
#             schema_editor.delete_model(table_name)
#
#         return JsonResponse({'message': f'Table "{table_name}" dropped successfully'}, status=200)
#     except Exception as e:
#         return JsonResponse({'error': f'Error dropping table: {str(e)}'}, status=500)
#
#
# @csrf_exempt
# def clear_entries_by_username(request):
#     username = request.POST.get('name', '')
#
#     if not username:
#         return JsonResponse({'error': 'Username is required'}, status=400)
#
#     try:
#         # Retrieve the user_id from the User table
#         user = User.objects.get(name=username)
#         user_id = user.id
#
#         # Clear entries from the OtherTable based on user_id
#         Activity.objects.filter(user_id=user_id).delete()
#
#         return JsonResponse({'message': f'Entries for user "{username}" cleared successfully'}, status=200)
#     except User.DoesNotExist:
#         return JsonResponse({'error': f'User "{username}" not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'error': f'Error clearing entries: {str(e)}'}, status=500)
#
#
@csrf_exempt
def get_activities_by_discipline_name(request):
    name = request.POST.get('discipline', '')

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
        return JsonResponse({'error': f'Discipline "{name}" not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error retrieving activities: {str(e)}'}, status=500)


@csrf_exempt
def add_activity(request):
    # Assuming you are receiving these values through a POST request
    user_id = request.POST.get('user_id', '')
    discipline_id = name_to_discipline_id(request.POST.get('discipline', ''))  # Convert the sport name to discipline_id
    elo = 1200  # Default elo value

    # Check if any required field is missing
    if not user_id or not discipline_id or not elo:
        return JsonResponse({'error': 'user_id, discipline_id, and elo are required fields'}, status=400)

    try:
        # Create a new entry in the Activity models
        user = Activity.objects.get(user_id=user_id, discipline_id=discipline_id)
        return JsonResponse({'error': 'User already has activity in this discipline'}, status=400)
    except:
        pass
    try:
        activity = Activity.objects.create(user_id=user_id, discipline_id=discipline_id, elo=elo)
        return JsonResponse({'message': 'Activity entry created successfully', 'activity_id': activity.activity_id}, status=200)
    except Exception as e:
        return JsonResponse({'error': f'Error creating activity entry: {str(e)}'}, status=500)


@csrf_exempt
def remove_activity(request):
    user_id = request.POST.get('user_id', '')
    discipline_id = name_to_discipline_id(request.POST.get('discipline', ''))

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
