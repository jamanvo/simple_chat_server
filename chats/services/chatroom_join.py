from datetime import datetime

import jwt
import pytz
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth.models import User

from chats.constants import CHATJOINUSER_STATUS_JOINED, CHATJOINUSER_STATUS_LEFT
from chats.models import ChatRoom, ChatJoinUser
from chats.services.chat_log import ChatLogService


class ChatRoomJoinService:
    def __init__(self):
        self.redis = settings.REDIS
        self.chatlog_service = ChatLogService()

    def join_chatroom(self, user: User, room_id: int) -> str | None:
        now = datetime.now(tz=pytz.UTC)

        if ChatJoinUser.objects.filter(user=user, chatroom_id=room_id, status=CHATJOINUSER_STATUS_JOINED).exists():
            return self._make_jwt(now)

        chatroom = ChatRoom.objects.get(id=room_id)

        added_join_count = self.redis.incrby(chatroom.join_count_redis_key, 1)
        if added_join_count > chatroom.max_join_count:
            self.redis.decrby(chatroom.join_count_redis_key, 1)
            return
        chatroom.incr_count()

        ChatJoinUser.objects.create(chatroom=chatroom, user=user, joined_at=now)
        self.chatlog_service.add_state_log(
            {"user_id": user.id, "room_id": room_id},
            "join",
            now.timestamp(),
        )

        return self._make_jwt(now)

    def left_chatroom(self, user_id: int, room_id: int) -> None:
        user = User.objects.get(pk=user_id)
        now = datetime.now(tz=pytz.UTC)
        chatroom = ChatRoom.objects.get(id=room_id)

        self.redis.decrby(chatroom.join_count_redis_key, 1)
        chatroom.decr_count()

        ChatJoinUser.objects.filter(
            chatroom=chatroom,
            user=user,
            status=CHATJOINUSER_STATUS_JOINED,
        ).update(
            status=CHATJOINUSER_STATUS_LEFT,
            left_at=now,
        )
        self.chatlog_service.add_state_log(
            {"user_id": user.id, "room_id": room_id},
            "left",
            now.timestamp(),
        )

    async def async_left_chatroom(self, user_id: int, room_id: int) -> None:
        await sync_to_async(self.left_chatroom)(user_id, room_id)

    def _make_jwt(self, now: datetime) -> str:
        payload = {"iss": "chatserver", "exp": now.timestamp()}
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    def reset_join_count(self, room_id: int):
        chatroom = ChatRoom.objects.get(id=room_id)
        self.redis.set(chatroom.join_count_redis_key, 0)
