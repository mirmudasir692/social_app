from django.db import models
from accounts.models import User, Follow
from django.db.models import Prefetch, Q, OuterRef, Exists


class StoryLodgerManager(models.Manager):

    def story_exists(self, user_id):
        return self.get_queryset().annotate(
            has_stories=Exists(
                Story.objects.filter(
                    storylodger_id=OuterRef("pk")
                )
            )
        ).filter(has_stories=True)

class StoryLodger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = StoryLodgerManager()

    def __str__(self):
        return self.user.username



class StoryManager(models.Manager):
    def create_story(self, file, user_id, caption):
        story_lodger, _ = StoryLodger.objects.get_or_create(user_id=user_id)
        story = self.create(file=file,caption=caption, storylodger=story_lodger)
        return story

    def get_stories(self, user_id, lodger_id=None):
        stories = self.filter( Q(storylodger__user_id=user_id) | Q(storylodger_id=lodger_id))
        return stories


class Story(models.Model):
    caption = models.CharField(max_length=500, null=True)
    file = models.FileField(upload_to="story")
    storylodger = models.ForeignKey(StoryLodger, on_delete=models.CASCADE)
    time = models.TimeField(auto_now_add=True)

    objects = StoryManager()
