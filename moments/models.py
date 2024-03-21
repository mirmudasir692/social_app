import random

from django.db import models
from accounts.models import User
import os
import uuid
import string
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import OuterRef, Prefetch, Exists


def create_custon_id(length=12):
    charecters = string.ascii_letters + string.digits
    id = "".join(random.choice(charecters) for _ in range(length))
    return id


class MomentManager(models.Manager):
    def get_moments(self, page, user):
        leaped_moments_exists = Leap.objects.filter(
            user=user,
            moment=OuterRef("pk")
        ).values("moment")

        moments = self.all().order_by("id").annotate(
            is_leaped = Exists(leaped_moments_exists)
        )
        return moments

    def get_moment(self, moment_id=None):
        if moment_id:
            moment = self.get(id=moment_id)
            return moment

    def delete_moment(self, id=None):
        try:
            if id:
                moment = self.get(id=id)
                moment.delete()
                video_path = moment.video.path
                if os.path.exists(video_path):
                    os.remove(video_path)
            else:
                raise ValueError("id is required")
        except Moment.DoesNotExist:
            raise ValueError("moment does't exist")


class Moment(models.Model):
    """
    this is the model which represent the moment which are short videos
    """
    id = models.CharField(primary_key=True, default=create_custon_id, editable=False, max_length=20)
    caption = models.CharField(max_length=510, verbose_name="Caption", blank=True)
    description = models.TextField(max_length=600, blank=True, verbose_name="Description")
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="moments")
    video = models.FileField(upload_to="moments", verbose_name="Video", max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    location = models.CharField(max_length=500, null=True, blank=True, )
    archive = models.BooleanField(default=False)
    tags = models.TextField(max_length=1000, blank=True)
    leaps = models.IntegerField(default=0)

    objects = MomentManager()

    class Meta:
        verbose_name = "Moment"
        verbose_name_plural = "Moments"

    def __str__(self):
        return self.id


class LeapManager(models.Manager):
    def like_moment(self, data , user_id):
        moment_id = data.get("moment_id")
        try:
            obj, created = self.get_or_create(moment_id=moment_id, user_id=user_id)
            print("hii")
            if not created:
                obj.delete()
        except IntegrityError:
            raise ValueError("Something went wrong")


class Leap(models.Model):
    """
    this is model table serves as like system for the Moment
    """
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name="moment_leaps")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_leaps")
    timespan = models.DateTimeField(auto_now_add=True)

    objects = LeapManager()

    class Meta:
        indexes = [
            models.Index(fields=['moment'], name='moment_idx')
        ]

    def __str__(self):
        return str(self.id)