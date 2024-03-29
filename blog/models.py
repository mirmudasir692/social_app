from django.db import models
from accounts.models import User, Follow


class BlogManager(models.Manager):

    def get_blogs(self, user_id):
        followed_user_ids = Follow.objects.filter(follower_id=user_id).values_list("followed_user_id", flat=True)
        blogs = self.filter(user_id__in=followed_user_ids)
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

