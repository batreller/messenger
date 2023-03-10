import json
import os
import random
from typing import Union
from threading import Thread
from django.http import JsonResponse, HttpResponse
from django.views.static import serve

from . import database, ws_methods


# def validate_token(token: str) -> JsonResponse:
#     if database.get_user_by_token(token):
#         return JsonResponse(status=200, data={"exists": True})
#     return JsonResponse(status=200, data={"exists": False})
from .data import users


def send_message(request) -> JsonResponse:
    try:
        token = request.COOKIES.get("session")
        token = safe_string(token)

        data = json.loads(request.body.decode('utf-8'))
        receiver = data.get("receiver")
        receiver = safe_string(receiver)

        text = data.get("text")
        text = safe_string(text)

        if not text or not receiver or not token:
            return JsonResponse(status=400, data={"success": False, "display_error": True,
                                                  "error_text": "Bad request, you should pass \"text\" and \"receiver\" to the data and token to the cookie"})

        user = database.get_user_by_token(token)
        receiver = database.get_user_by_id(receiver)
        if not user:
            return JsonResponse(status=401,
                                data={"success": False, "display_error": True, "error_text": "Log into your account"})
        if not receiver:
            return JsonResponse(status=400, data={"success": False, "display_error": True,
                                                  "error_text": "Receiver does not exists"})

        database.send_message(text, user[0], receiver[0])

        user_connection = users.get(receiver[0])
        if user_connection:
            json_message = {
                "action": "NEW_MESSAGE",
                "from_user_id": user[0],
                "text": text
            }
            user_connection.send(text_data=json.dumps(json_message))

        return JsonResponse(status=200, data={"success": True})

    except json.decoder.JSONDecodeError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})
    except KeyError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "cookie can not be null"})


def get_chats(request) -> JsonResponse:
    try:
        token = request.COOKIES.get("session")
        token = safe_string(token)

        user = database.get_user_by_token(token)
        if not user:
            return JsonResponse(status=401,
                                data={"success": False, "display_error": True, "error_text": "Log into your account"})

        chats = database.get_chats_by_id(user[0])
        return JsonResponse(status=200, data={"success": True, "chats": chats})

    except json.decoder.JSONDecodeError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})
    except KeyError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "cookie can not be null"})


def get_users_chats(request) -> JsonResponse:
    try:
        token = request.COOKIES.get("session")
        token = safe_string(token)

        user = database.get_user_by_token(token)

        user_1 = int(request.GET.get("user_1"))
        user_1 = safe_string(user_1)

        user_2 = int(request.GET.get("user_2"))
        user_2 = safe_string(user_2)

        if user[0] != user_1 and user[0] != user_2:
            return JsonResponse(status=401,
                                data={"success": False, "display_error": True,
                                      "error_text": "You have no access to the messages"})

        if not user:
            return JsonResponse(status=401,
                                data={"success": False, "display_error": True, "error_text": "Log into your account"})

        if user_1 is None or user_2 is None or not token:
            return JsonResponse(status=400, data={"success": False, "display_error": True,
                                                  "error_text": "Bad request, you should pass \"user_1\" and \"user_2\" to the data and token to the cookie"})

        messages = database.get_users_chats(user_1, user_2)
        return JsonResponse(status=200, data={"success": True, "messages": messages})

    except json.decoder.JSONDecodeError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})
    except KeyError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})


def register(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode('utf-8'))
        login = data.get("login")
        login = safe_string(login)

        password = data.get("password")
        password = safe_string(password)

        user = database.get_user_by_login(login)
        if user:
            return JsonResponse(status=200, data={"success": False, "display_error": True,
                                                  "error_text": "User with this login already exists"})

        if not login or not password:
            return JsonResponse(status=400, data={"success": False, "display_error": True,
                                                  "error_text": "login and password can not be blank, you should send request as {\"login\": \"login\", \"password\": \"password\"}"})

        token = "".join(
            [random.choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789") for _ in range(30)])
        database.register(token, login, password)
        user = database.get_user_by_token(token)
        return JsonResponse(status=200, data={"success": True, "token": token, "user_id": user[0]})

    except json.decoder.JSONDecodeError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})
    except KeyError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "cookie can not be null"})


def login(request) -> JsonResponse:
    try:
        login = request.GET.get("login")
        login = safe_string(login)

        password = request.GET.get("password")
        password = safe_string(password)

        user = database.get_user_by_login(login)
        if not user:
            return JsonResponse(status=200,
                                data={"success": False, "display_error": True, "error_text": "User does not exists"})

        if not login or not password:
            return JsonResponse(status=400, data={"success": False, "display_error": True,
                                                  "error_text": "login and password can not be blank, you should send request as {\"login\": \"login\", \"password\": \"password\"}"})

        user = database.get_user_by_login(login)
        return JsonResponse(status=200, data={"success": True, "token": user[6], "user_id": user[0]})

    except json.decoder.JSONDecodeError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})
    except KeyError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "cookie can not be null"})


def get_all_users(request) -> JsonResponse:
    try:
        token = request.COOKIES.get("session")
        token = safe_string(token)

        search_filter = request.GET.get("search")

        user = database.get_user_by_token(token)

        if not user:
            return JsonResponse(status=401,
                                data={"success": False, "display_error": True, "error_text": "Log into your account"})

        users = database.get_all_users(search_filter, user[0])
        return JsonResponse(status=200, data={"success": True, "users": users})

    except json.decoder.JSONDecodeError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})
    except KeyError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})


def change_name(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode('utf-8'))
        name = data.get("name")
        name = safe_string(name)

        token = request.COOKIES.get("session")
        token = safe_string(token)

        user = database.get_user_by_token(token)

        if not user:
            return JsonResponse(status=401,
                                data={"success": False, "display_error": True, "error_text": "Log into your account"})
        if not name:
            return JsonResponse(status=400,
                                data={"success": False, "display_error": True,
                                      "error_text": "You should pass \"name\" param"})

        database.set_name(user[0], name)

        json_message = {
            "action": "USER_CHANGED_NAME",
            "user_id": user[0],
            "new_name": name,
            "message": "user change his name"
        }

        Thread(target=ws_methods.spam_related_users, args=(user[0], json_message,)).start()

        return JsonResponse(status=200, data={"success": True, "message": "Name successfully changed"})

    except json.decoder.JSONDecodeError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})
    except KeyError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})


def change_avatar(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode('utf-8'))
        avatar = data.get("avatar")
        avatar = safe_string(avatar)

        token = request.COOKIES.get("session")
        token = safe_string(token)

        user = database.get_user_by_token(token)

        if not user:
            return JsonResponse(status=401,
                                data={"success": False, "display_error": True, "error_text": "Log into your account"})
        if not avatar:
            return JsonResponse(status=400,
                                data={"success": False, "display_error": True,
                                      "error_text": "You should pass \"avatar\" param the value is base64 image"})

        database.set_avatar(user[0], avatar)

        json_message = {
            "action": "USER_CHANGED_AVATAR",
            "user_id": user[0],
            "new_avatar": avatar,
            "message": "user change his avatar"
        }

        Thread(target=ws_methods.spam_related_users, args=(user[0], json_message,)).start()

        return JsonResponse(status=200, data={"success": True, "message": "Avatar successfully changed"})

    except json.decoder.JSONDecodeError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})
    except KeyError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})


def api_export(request) -> HttpResponse:
    try:
        token = request.COOKIES.get("session")
        token = safe_string(token)
        user = database.get_user_by_token(token)

        if not user or user[0] != 1:
            return JsonResponse(
                {"success": False, "message": "you have no access to the method, how do you even find it?"})

        filepath = 'users.db'
        return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    except KeyError:
        return JsonResponse({"success": False, "message": "you have no access to the method, how do you even find it?"})


def get_me(request) -> JsonResponse:
    try:
        token = request.COOKIES.get("session")
        token = safe_string(token)
        user = database.get_user_by_token(token)
        if not user:
            return JsonResponse(status=401, data={"success": False, "display_error": True,
                                                  "error_text": "Invalid token"})

        return JsonResponse(status=200, data={"success": True, "user": [user[0], user[3], user[5], user[4]]})
    except KeyError:
        return JsonResponse(status=400, data={"success": False, "display_error": True,
                                              "error_text": "content-type = application/json, pass data as raw"})


def safe_string(text: Union[str, int]) -> Union[int, str, None]:
    if not text:
        return None
    if type(text) == int:
        return text

    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
