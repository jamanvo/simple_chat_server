from django.urls import re_path

from chats.services.application.consumer import ChatConsumerApplication

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_id>\d+)/$", ChatConsumerApplication.as_asgi()),
]
