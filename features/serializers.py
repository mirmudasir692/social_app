from rest_framework import serializers
from .models import Basket, Save
from accounts.serializers import UserPartitionSerializer
from moments.serializers import MomentSerializer
from blog.serializers import BlogSerializer


class BasketSerializer(serializers.ModelSerializer):
    moment = MomentSerializer(required=False)
    user = UserPartitionSerializer(write_only=True, required=False)

    class Meta:
        model = Basket
        fields = ["id", "moment", "user"]

    @classmethod
    def add_to_basket(cls, validated_data, user_id):
        moment_id = validated_data.get("moment_id", None)
        basket_item = Basket.objects.add_to_basket(moment_id, user_id)
        return basket_item


class SaveBlogSerializer(serializers.ModelSerializer):
    user = UserPartitionSerializer(required=False)
    blog = BlogSerializer(required=False)
    """
    serializer for save
    """
    class Meta:
        model = Save
        fields = ["id", "user", "blog"]

    @classmethod
    def save_blog(cls, user_id, data):
        saved_instance = Save.objects.save_blog(user_id, data)
        return saved_instance
