from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.middleware.csrf import get_token
from .models import User


# @csrf_exempt
# def my_view(request):
#     @csrf_protect
#     def protected_path(request):
#         do_something()
#
#     if some_condition():
#         return protected_path(request)
#     else:
#         do_something_else()


@csrf_protect
def simulate_csrf_error(request):
    if request.method == 'POST':
        return HttpResponse("Form submitted successfully!")
    return HttpResponse("GET request, please submit the form.")


@csrf_protect
def add_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        User.objects.create(name=name, email=request.POST.get('email'))
        return JsonResponse({'message': 'User added successfully'})
    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def get_users(request):
    users = User.objects.values()
    return JsonResponse(list(users), safe=False)


@csrf_exempt
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})
