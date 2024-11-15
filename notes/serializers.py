from rest_framework import serializers
from .models import Note
from accounts.serializers import UserPartitionSerializer


class NoteSerializer(serializers.ModelSerializer):
    user = UserPartitionSerializer(required=False)
    added_on = serializers.DateTimeField(required=False)

    class Meta:
        model = Note
        fields = ("id", "user", "text", "added_on")

    @classmethod
    def create_note(cls, data, user_id):
        return NoteSerializer(Note.objects.add_note(data, user_id))

    @classmethod
    def update_note(cls, data, user_id):
        return NoteSerializer(Note.objects.update_note(data, user_id))
