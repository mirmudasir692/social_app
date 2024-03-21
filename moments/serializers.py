from rest_framework import serializers
from accounts.serializers import UserPartitionSerializer
from .models import Moment, Leap


class MomentSerializer(serializers.ModelSerializer):
    publisher = UserPartitionSerializer()
    caption = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(read_only=True)
    location = serializers.CharField(required=False)
    tags = serializers.CharField(required=False)
    is_leaped = serializers.BooleanField(required=False)
    class Meta:
        model = Moment
        fields = ("id", "caption", "description", "publisher", "video",
                  "timestamp", "location", "archive", "tags", "leaps", "is_leaped")


class LeapSerializer(serializers.ModelSerializer):
    moment = MomentSerializer(required=False)
    user = UserPartitionSerializer(required=False)
    timespan = serializers.DateTimeField(required=False)

    class Meta:
        model = Leap
        fields = ["id", "moment", "user", "timespan"]
