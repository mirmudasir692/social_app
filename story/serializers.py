from rest_framework import serializers
from .models import Story, StoryLodger
from accounts.serializers import UserPartitionSerializer
from rest_framework.exceptions import ValidationError


class StoryLodgerSerializer(serializers.ModelSerializer):
    user = UserPartitionSerializer(required=False)

    class Meta:
        model = StoryLodger
        fields = ["id", "user"]


class StorySerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()  # Use SerializerMethodField for custom logic
    storylodger = StoryLodgerSerializer(required=False, write_only=True)
    time = serializers.TimeField(required=False)
    user = UserPartitionSerializer(required=False)
    caption = serializers.CharField(required=False)

    class Meta:
        model = Story
        fields = ["id", "file", "storylodger", "time", "user", "caption"]

    def get_file(self, obj):
        # Custom method to get the file path
        return obj.file.url if obj.file else None

    @classmethod
    def create_story(self, validated_data, user_id):
        file = validated_data.get("file", None)
        caption = validated_data.get("caption", None)
        if not file:
            raise ValidationError("please provide file")
        story = Story.objects.create_story(file, user_id, caption)
        return story


class PaginatorSerializer(serializers.Serializer):
    stories = StorySerializer(required=False, many=True)
    has_next = serializers.BooleanField(required=False)
    has_previous = serializers.BooleanField(required=False)
