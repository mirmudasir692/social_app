from rest_framework import serializers
from .models import Basket, Save
from accounts.serializers import UserPartitionSerializer
from moments.serializers import MomentSerializer
from blog.serializers import BlogSerializer


class BasketSerializer(serializers.ModelSerializer):
    moment = MomentSerializer(required=False, many=True)
    user = UserPartitionSerializer(write_only=True, required=False)

    class Meta:
        model = Basket
        fields = ["id", "moment", "user"]

    @classmethod
    def add_to_basket(cls, validated_data, user_id):
        moment_id = validated_data.get("moment_id", None)
        basket_item = Basket.objects.add_to_basket(moment_id, user_id)
        return basket_item

    @classmethod
    def get_my_basket(cls, user_id):
        my_basket = cls(Basket.objects.get_my_basket(user_id), many=True)
        print("serializer", my_basket)
        return my_basket


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

    @classmethod
    def get_blogs(cls, user_id):
        return cls(Save.objects.get_saved_blogs(user_id), many=True)
