from django.urls import re_path

from chats.services.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<title>\w+)/$", ChatConsumer.as_asgi()),
]
