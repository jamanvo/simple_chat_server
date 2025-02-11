from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.models import User

from chats.services.domain.chatroom_join import ChatRoomJoinDomain
from chats.services.domain.state_log import ChatLogService


class ChatRoomJoinApplication:
    def __init__(self):
        self.redis = settings.REDIS
        self.log_service = ChatLogService()
        self.join_domain = ChatRoomJoinDomain()

    def join_chatroom(self, user: User, room_id: int) -> str | None:
        now = datetime.now(tz=pytz.UTC)
        token = self.join_domain.join_chatroom(user, room_id, now)
        self.log_service.add_join_log(user.id, room_id, now.timestamp())

        return token

    def left_chatroom(self, user_id: int, room_id: int) -> None:
        now = datetime.now(tz=pytz.UTC)
        self.join_domain.left_chatroom(user_id, room_id, now)
        self.log_service.add_left_log(user_id, room_id, now.timestamp())
