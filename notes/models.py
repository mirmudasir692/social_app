from django.db import models
from accounts.models import User
from accounts.models import Follow


class NoteManager(models.Manager):
    def add_note(self, data, user_id):
        text = data.get("text", None)
        audio = data.get("audio", None)
        note_instance = self.create(text=text, user_id=user_id, audio=audio)
        return note_instance

    def get_notes(self, user_id):
        followed_user_ids = Follow.objects.filter(follower_id=user_id).values_list("followed_user_id", flat=True)
        print("followed", followed_user_ids)
        notes = self.filter(user_id__in=followed_user_ids)
        print("notes", notes)
        return notes


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, )
    audio = models.FileField(upload_to="notes_audio", null=True)
    added_on = models.DateTimeField(auto_now=True)

    objects = NoteManager()

    def __str__(self):
        return self.user.username
