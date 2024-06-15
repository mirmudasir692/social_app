from django.db import models
import uuid
from accounts.models import User
from accounts.models import Follow
from django.db.models import OuterRef, Exists
from django.core.paginator import Paginator


class PostManager(models.Manager):

    def get_posts(self, user_id, page_num):

        followed_user_ids = Follow.objects.filter(follower_id=user_id).values_list("followed_user_id", flat=True)
        posts = self.filter(owner_id__in=followed_user_ids)
        paginator = Paginator(posts, 4)
        posts = paginator.get_page(page_num)
        return posts, posts.has_previous(), posts.has_next()

    def upload_post(self, user_id, data):
        caption = data.get("caption", "")
        image = data.get("image", None)
        post_instance = self.create(caption=caption, owner_id=user_id, image=image)
        return post_instance

    def like_post(self, user_id, post_id):
        print("post_id", post_id)

        like_instance, created = LikePost.objects.get_or_create(post_id=post_id, user_id=user_id)
        post = self.get(unique_id=post_id)

        if not created:
            like_instance.delete()
            post.num_likes -= 1
            post.save()
            return False
        elif like_instance:
            post.num_likes += 1
            post.save()
            return True
        else:
            return False


class Post(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    caption = models.TextField(blank=True, max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="posts")
    image = models.ImageField(upload_to="posts", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    archive = models.BooleanField(default=False)
    num_likes = models.IntegerField(default=0, db_default=0)

    objects = PostManager()

    def __str__(self):
        return f"{self.unique_id}"


class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")

    def __str__(self):
        return f"{self.post.unique_id}"


