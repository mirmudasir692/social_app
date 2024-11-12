from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from accounts.models import User, Follow
from story.models import StoryLodger
from django.db import transaction


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        story_lodger = StoryLodger.objects.create(user=instance)
        return story_lodger

@receiver(post_save, sender=Follow)
def update_users_after_follow(sender, instance, created, **kwargs):
    """
    this function used for updating follower and following lists of the users
    :return:
    """
    if created:
        with transaction.atomic():
            instance.follower.following_num += 1
            instance.follower.save()
            instance.followed_user.followers_num += 1
            instance.followed_user.save()

@receiver(post_delete, sender=Follow)
def update_users_after_unfollow(sender, instance, using, **kwargs):
    with transaction.atomic():
        if instance.follower.following_num >0:
            instance.follower.following_num -= 1
            instance.follower.save()
        if instance.followed_user.followers_num >0:
            instance.followed_user.followers_num -= 1
            instance.followed_user.save()

