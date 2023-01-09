# from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.temp),
    path('login', views.login),
    path('chats', views.chats),
    path('settings', views.settings),

    # path('api/validate_token/<str:token>', views.validate_token),
    # path('api/chats/<str:token>', views.chats),
    path('api/message', views.send_message),
    path('api/get_me', views.get_me),
    path('api/chats', views.get_chats),
    path('api/get_users_chats', views.get_users_chats),
    path('api/register', views.api_register),
    path('api/login', views.api_login),
    path('api/all_users', views.api_all_users),
    path('api/change_name', views.change_name),
    path('api/change_avatar', views.change_avatar),
    path('api/export', views.api_export),
]
