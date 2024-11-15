from django.db import models
from accounts.models import User
from accounts.models import Follow
from django.db.models import Q


class NoteManager(models.Manager):
    def add_note(self, data, user_id):
        text = data.get("text", None)
        note_instance = self.create(text=text, user_id=user_id)
        return note_instance

    def get_notes(self, user_id):
        followed_user_ids = Follow.objects.filter(follower_id=user_id).values_list("followed_user_id", flat=True)
        print("followed", followed_user_ids)
        notes = self.filter(Q(user_id=user_id) | Q(user_id__in=followed_user_ids))
        print("notes", notes)
        return notes

    def update_note(self, data, user_id):
        text = data.get("text", "")
        note = self.filter(user_id=user_id)[0]
        note.text = text
        note.save()
        return note


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, )
    added_on = models.DateTimeField(auto_now=True)

    objects = NoteManager()

    def __str__(self):
        return self.user.username
