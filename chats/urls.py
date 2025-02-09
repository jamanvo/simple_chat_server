from django.urls import path

from chats import views

app_name = "chats"
urlpatterns = [
    path("<int:room_id>/join/", views.join, name="join"),
    path("<int:room_id>/left/", views.left, name="left"),
    path("chatroom/", views.chatroom, name="chatroom"),
]
