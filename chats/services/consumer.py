import datetime
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chats.services.chat_log import ChatLogService


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chatroom_group = ""
        self.chatlog_service = ChatLogService()

    async def connect(self):
        title = self.scope["url_route"]["kwargs"]["title"]
        self.chatroom_group = f"chatroom_{title}"

        await self.channel_layer.group_add(self.chatroom_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chatroom_group, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if self._is_over_length_message(text_data_json):
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
        await self.chatlog_service.add_message(text_data_json, ts)

        send_message = dict(**text_data_json, **{"type": "chat_message"})
        await self.channel_layer.group_send(self.chatroom_group, send_message)

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
