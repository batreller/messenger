import json
import traceback
from threading import Thread

from channels.generic.websocket import WebsocketConsumer

from . import ws_methods
from .data import *


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_token = None
        self.user_id = None
        self.verified = False
        self.verification_timeout = 1  # seconds
        self.verification_timer = threading.Timer(self.verification_timeout, self.close_if_not_verified)
        self.verification_timer.start()

    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            "message": "waiting for authorization"
        }))

        # users[self] = {"verified": False, "user_id": None, "user_token": None}

    def close_if_not_verified(self):
        if not self.verified:
            self.close(4000)  # close code for "not verified"

    def receive(self, text_data=None, bytes_data=None):
        try:
            json_data = json.loads(text_data)
        except:
            print(traceback.format_exc())
            self.close()
            return

        if not self.verified:
            user_token = json_data.get("token")
            if not user_token:
                self.close()
                return

            user = ws_methods.get_user_by_token(user_token)
            if not user:
                self.close()
                return

            self.verified = True
            self.user_token = user_token
            self.user_id = user[0]
            users[user[0]] = self
            ws_methods.change_online(True, self.user_id)

            json_message = {
                "action": "ACTIVITY_UPDATE",
                "user_id": user[0],
                "is_online": True,
                "message": "user change his activity status"
            }
            ws_methods.spam_related_users(user[0], json_message)

    def disconnect(self, code):
        Thread(target=ws_methods.change_online, args=(True, self.user_id,)).start()

        print(self, code, 'disconnected')
        # delete users[user_id]
        if users.get(self.user_id):
            del users[self.user_id]

        # delete users[ws_session]
        # del users[self]
        self.close()
