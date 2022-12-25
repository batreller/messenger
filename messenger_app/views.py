from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import api_methods
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    return render(request, "html/index.html")

# @csrf_exempt
# def validate_token(request, token):
    # return api_methods.validate_token(token)

# def chats(request, token):
#     return JsonResponse(api_methods.chats(token))

@csrf_exempt
def login(request):
    return render(request, "html/login.html")

@csrf_exempt
def chats(request):
    return render(request, "html/chats.html")

@csrf_exempt
def settings(request):
    return render(request, "html/settings.html")

@csrf_exempt
def send_message(request):
    return api_methods.send_message(request)

@csrf_exempt
def get_me(request):
    return api_methods.get_me(request)

@csrf_exempt
def get_chats(request):
    return api_methods.get_chats(request)

@csrf_exempt
def get_users_chats(request):
    return api_methods.get_users_chats(request)

@csrf_exempt
def api_register(request):
    return api_methods.register(request)

@csrf_exempt
def api_login(request):
    return api_methods.login(request)

@csrf_exempt
def api_all_users(request):
    return api_methods.get_all_users(request)

@csrf_exempt
def change_avatar(request):
    return api_methods.change_avatar(request)

@csrf_exempt
def change_name(request):
    return api_methods.change_name(request)

@csrf_exempt
def api_export(request):
    return api_methods.api_export(request)
