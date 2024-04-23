from rest_framework import serializers
from .models import Blog, Like, Comment
from accounts.serializers import UserPartitionSerializer


class BlogSerializer(serializers.ModelSerializer):
    user = UserPartitionSerializer(required=False)
    likes = serializers.IntegerField(read_only=True)
    comments = serializers.IntegerField(read_only=True)
    timestamp = serializers.DateTimeField(required=False)
    is_liked = serializers.BooleanField(required=False)
    is_saved = serializers.BooleanField(required=False)

    class Meta:
        model = Blog
        fields = ["id", "title", "content", "user", "likes", "comments", "timestamp", "is_liked", "is_saved"]

    @classmethod
    def create_blog(cls, data, user_id):
        blog = Blog.objects.create_blog(data, user_id)
        return blog


class CommentSerializer(serializers.ModelSerializer):
    user = UserPartitionSerializer(required=False)
    class Meta:
        model = Comment
        fields = ["id", "content", "user", "timestamp"]

    @classmethod
    def add_comment(cls, data, user_id):
        return Comment.objects.create_comment(data, user_id)
