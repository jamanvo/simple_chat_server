from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chats.services.application.chat_join import ChatRoomJoinApplication


@login_required
@api_view(["POST"])
def token(request):
    token, _ = Token.objects.get_or_create(user=request.user)
    return Response({"token": token.key})


@api_view(["POST"])
def join(request, room_id: int):
    data = ChatRoomJoinApplication().join_chatroom(request.user, room_id)
    return Response({"token": data})


@api_view(["DELETE"])
def left(request, room_id: int):
    ChatRoomJoinApplication().left_chatroom(request.user.id, room_id)
    return Response()


@login_required(login_url="/admin/login/")
def chatroom(request):
    return render(request, "chatroom.html")
