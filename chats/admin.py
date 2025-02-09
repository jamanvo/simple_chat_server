from django.contrib import admin

from chats.models import ChatRoom, ChatJoinUser


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "max_join_count",
    )


@admin.register(ChatJoinUser)
class ChatJoinUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "chatroom",
        "user",
        "status",
    )
