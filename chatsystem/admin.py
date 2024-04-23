from django.contrib import admin
from .models import MessageGroup, Message


@admin.register(MessageGroup)
class MessageGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "user1", "user2")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver")
