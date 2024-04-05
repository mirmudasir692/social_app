from django.db import models
from accounts.models import User
from moments.models import Moment
from blog.models import Blog


class BasketManager(models.Manager):
    def add_to_basket(self, moment_id, user_id):
        try:
            basket_item, created = self.get_or_create(moment_id=moment_id, user_id=user_id)
            if not created:
                basket_item.delete()
            return basket_item
        except self.model.DoesNotExist:
            raise ValueError("Moment doest exist")

class Basket(models.Model):
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name="bucketed_moments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_moments")


    objects = BasketManager()
    def __str__(self):
        return str(self.id)


class SaveManager(models.Manager):
    def save_blog(self, user_id, blog_id):
        return self.create(user_id=user_id, blog_id=blog_id)


class Save(models.Model):
    """
    for saving blogs
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_blogs")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="saves"),

    def __str__(self):
        return self.user.username
