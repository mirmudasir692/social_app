from django.contrib import admin
from .models import Blog, Like, Comment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "timestamp")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "blog", "timestamp")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "user", "blog", "timestamp")