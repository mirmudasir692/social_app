from rest_framework import serializers
from .models import Blog
from accounts.serializers import UserPartitionSerializer


class BlogSerializer(serializers.ModelSerializer):
    user = UserPartitionSerializer(required=False)
    likes = serializers.IntegerField(read_only=True)
    comments = serializers.IntegerField(read_only=True)
    timestamp = serializers.DateTimeField(required=False)

    class Meta:
        model = Blog
        fields = ["id", "title", "content", "user", "likes", "comments", "timestamp"]

    @classmethod
    def create_blog(cls, data, user_id):
        blog = Blog.objects.create_blog(data, user_id)
        return blog