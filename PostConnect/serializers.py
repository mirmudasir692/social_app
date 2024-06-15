from rest_framework import serializers
from .models import Post, LikePost
from accounts.serializers import UserPartitionSerializer


class PostSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(required=True)
    owner = UserPartitionSerializer(required=False)
    image = serializers.ImageField(required=True)
    created_at = serializers.DateTimeField(required=False)
    archive = serializers.BooleanField(required=False)
    like = serializers.SerializerMethodField(required=False)
    num_likes = serializers.IntegerField(required=False)

    class Meta:
        model = Post
        fields = ["unique_id", "caption", "owner", "image", "created_at", "archive", "like", "num_likes"]

    @classmethod
    def create_post(cls, data, user_id):
        return cls(Post.objects.upload_post(user_id, data))

    def get_like(self, obj):
        request = self.context.get('request')
        print("request", request)
        try:
            return LikePost.objects.filter(post=obj, user=request.user).exists()
        except Exception as e:
            print("Error:", str(e))
        print("none")
        return False


class PostsWithPagination(serializers.Serializer):
    posts = PostSerializer(many=True)
    has_previous = serializers.BooleanField()
    has_next = serializers.BooleanField()


class LikePostSerializer(serializers.ModelSerializer):
    post = PostSerializer(required=False)
    user = UserPartitionSerializer(required=False)

    class Meta:
        model = LikePost
        fields = ["id", "post", "user"]

    @classmethod
    def create_like(cls, data, user_id):
        post_id = data.get("post_id")
        return Post.objects.like_post(user_id, post_id)
