from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User
from story.models import StoryLodger


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        story_lodger = StoryLodger.objects.create(user=instance)
        return story_lodger