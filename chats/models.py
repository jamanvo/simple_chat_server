from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F

from chats.constants import (
    CHATROOM_STATUS_CHOICES,
    CHATROOM_STATUS_WAIT,
    CHATJOINUSER_STATUS_CHOICES,
    CHATJOINUSER_STATUS_JOINED,
)


class ChatRoom(models.Model):
    title = models.CharField(max_length=255)
    status = models.IntegerField(choices=CHATROOM_STATUS_CHOICES, default=CHATROOM_STATUS_WAIT)
    join_count = models.IntegerField(default=0)
    max_join_count = models.IntegerField(
        default=2,
        validators=[MaxValueValidator(100), MinValueValidator(2)],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def join_count_redis_key(self) -> str:
        return f"chatroom:{self.id}:join-count"

    def incr_count(self) -> None:
        self.join_count = F("join_count") + 1
        self.save(update_fields=["join_count", "updated_at"])

    def decr_count(self) -> None:
        self.join_count = F("join_count") - 1
        self.save(update_fields=["join_count", "updated_at"])


class ChatJoinUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    status = models.IntegerField(choices=CHATJOINUSER_STATUS_CHOICES, default=CHATJOINUSER_STATUS_JOINED)

    joined_at = models.DateTimeField()
    left_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
