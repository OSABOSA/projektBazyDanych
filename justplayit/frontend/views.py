from django.shortcuts import render

# Create your views here.

# views.py
from django.http import JsonResponse
from .models import User


def add_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        User.objects.create(name=name, email=request.POST.get('email'))
        return JsonResponse({'message': 'User added successfully'})
    return JsonResponse({'error': 'Invalid request method'})


def get_users(request):
    users = User.objects.values()
    return JsonResponse(list(users), safe=False)


