import datetime
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chats.services.chat_log import ChatLogService
from chats.services.chatroom_join import ChatRoomJoinService


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chatroom_group = ""
        self.chatlog_service = ChatLogService()
        self.chat_join_service = ChatRoomJoinService()
        self.user_id = None
        self.room_id = None

    async def connect(self):
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.chatroom_group = f"chatroom_{room_id}"
        self.room_id = room_id

        await self.channel_layer.group_add(self.chatroom_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.chat_join_service.async_left_chatroom(self.user_id, self.room_id)
        await self.channel_layer.group_discard(self.chatroom_group, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data["type"] == "auth":
            await self.set_auth(data)
            return

        if self._is_over_length_message(data):
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "error_message": "메시지 길이가 너무 깁니다.",
                    }
                )
            )
            return

        ts = datetime.datetime.now(datetime.UTC).timestamp()
        await self.chatlog_service.add_message(data, ts)

        send_message = dict(**data, **{"type": "chat_message"})
        await self.channel_layer.group_send(self.chatroom_group, send_message)

    async def set_auth(self, data: dict):
        self.user_id = data["user_id"]

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "message": event["message"],
                    "user_name": event["user_name"],
                    "user_id": event["user_id"],
                }
            )
        )

    def _is_over_length_message(self, text_data_json: dict) -> bool:
        return len(text_data_json["message"]) > 10
