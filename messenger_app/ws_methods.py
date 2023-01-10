import json
from typing import Union

from messenger_app import database
from messenger_app.data import users


def get_user_by_token(token: str) -> Union[tuple, bool]:
    user = database.get_user_by_token(token)
    if user:
        return user
    return False


def get_related_users(to_user_id: int) -> list:
    related_users = database.get_related_users(to_user_id)
    related_users = [user[0] for user in related_users]
    return related_users


def send_message_to_users(users_list: list[int], json_message: dict) -> None:
    for user_index in users_list:
        user_connection = users.get(user_index)
        if user_connection:
            user_connection.send(text_data=json.dumps(json_message))


def spam_related_users(related_to_user_id: int, json_message: dict) -> None:
    related_users = get_related_users(related_to_user_id)
    send_message_to_users(related_users, json_message)


def change_online(status: bool, user_id: int) -> None:
    database.change_online(status, user_id)

    json_message = {
        "action": "ACTIVITY_UPDATE",
        "user_id": user_id,
        "is_online": False,
        "message": "user change his activity status"
    }
    spam_related_users(user_id, json_message)


def safe_string(text: Union[str, int]) -> Union[int, str, None]:
    if not text:
        return None
    if type(text) == int:
        return text

    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
