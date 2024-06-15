from django.contrib import admin
from .models import Post, LikePost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("unique_id", "caption", "owner", "image", "created_at", "archive")


@admin.register(LikePost)
class LikePost(admin.ModelAdmin):
    list_display = ("id", "post", "user")
