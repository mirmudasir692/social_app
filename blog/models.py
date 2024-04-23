from django.db import models
from accounts.models import User, Follow
from django.db import transaction
from django.db.models import OuterRef, Exists


class BlogManager(models.Manager):

    def get_blogs(self, user_id):
        from features.models import Save
        liked_blog_exists = Like.objects.filter(
            user_id=user_id,
            blog=OuterRef("pk")
        ).values()
        saved_blog_exists = Save.objects.filter(
            user_id=user_id,
            blog=OuterRef("pk")
        ).values()

        followed_user_ids = Follow.objects.filter(follower_id=user_id).values_list("followed_user_id", flat=True)
        blogs = self.filter(user_id__in=followed_user_ids).annotate(
            is_liked=Exists(liked_blog_exists),
            is_saved=Exists(saved_blog_exists),
        )
        return blogs

    def create_blog(self, data, user_id):
        title = data.get("title", None)
        content = data.get("content", None)
        blog = self.create(user_id=user_id, title=title, content=content)
        blog.save()
        return blog

    def delete_blog(self, blog_id, user_id):
        try:
            blog = self.get(id=blog_id)
            if blog.user.id == user_id:
                blog.delete()
                return True
            raise ValueError("you don't have permission to delete this")
        except self.model.DoesNotExist:
            raise ValueError("blog is already deleted")


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_blogs")
    title = models.CharField(max_length=500, null=True)
    content = models.TextField(max_length=2000)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BlogManager()

    def __str__(self):
        return self.title


class LikeManager(models.Manager):
    def like_blog(self, user_id, blog_id):
        with transaction.atomic():
            like_instance, created = self.get_or_create(user_id=user_id, blog_id=blog_id)
            blog = Blog.objects.select_for_update().get(id=blog_id)
            if created:
                blog.likes += 1
            else:
                blog.likes -= 1
                like_instance.delete()
            blog.save()
            if created:
                return True


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_likes")
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = LikeManager()

    def __str__(self):
        return self.user.username


class CommentManager(models.Manager):
    def create_comment(self, data ,user_id):
        content = data.get("content", None)
        blog_id = data.get("blog_id", None)
        if not content:
            raise ValueError("please provide content")
        if not blog_id:
            raise ValueError("blog id is highly needed")
        return self.create(content=content, user_id=user_id, blog_id=blog_id)
    def get_comments(self, blog_id):
        comments = self.filter(blog_id=blog_id)
        return comments


class Comment(models.Model):
    content = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return self.user.username
