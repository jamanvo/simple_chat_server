from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chats.services.chatroom_join import ChatRoomJoinService


@login_required
@api_view(["POST"])
def join(request, room_id: int):
    data = ChatRoomJoinService().join_chatroom(request.user, room_id)
    return Response({"token": data})


@login_required
@api_view(["DELETE"])
def left(request, room_id: int):
    ChatRoomJoinService().left_chatroom(request.user, room_id)
    return Response()


@login_required
@api_view(["GET"])
def user_state(request, room_id: int, user_id: int):
    return Response()


@login_required(login_url="/admin/login/")
def chatroom(request):
    return render(request, "chatroom.html")
