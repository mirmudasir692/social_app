from rest_framework import serializers
from accounts.serializers import UserPartitionSerializer
from .models import Moment, Leaf, Fruit


class MomentSerializer(serializers.ModelSerializer):
    publisher = UserPartitionSerializer()
    caption = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(read_only=True)
    location = serializers.CharField(required=False)
    tags = serializers.CharField(required=False)
    is_leaped = serializers.BooleanField(required=False)
    is_basked = serializers.BooleanField(required=False)

    class Meta:
        model = Moment
        fields = ("id", "caption", "description", "publisher", "video",
                  "timestamp", "location", "archive", "tags", "leaps", "is_leaped", "is_basked")


class LeapSerializer(serializers.ModelSerializer):
    moment = MomentSerializer(required=False)
    user = UserPartitionSerializer(required=False)
    timespan = serializers.DateTimeField(required=False)

    class Meta:
        model = Leaf
        fields = ["id", "moment", "user", "timespan"]


class FruitSerializer(serializers.ModelSerializer):
    timespan = serializers.DateTimeField(required=False)
    moment = MomentSerializer(required=False, write_only=True)
    user = UserPartitionSerializer(required=False)

    class Meta:
        model = Fruit
        fields = ["id", "content", "user", "moment", "timespan"]

    @classmethod
    def create_fruit(cls, validated_data, user_id):
        print()
        fruit = Fruit.objects.make_fruit(validated_data, user_id)
        return fruit
