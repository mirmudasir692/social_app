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

    def get_my_basket(self, user_id):
        print(user_id)
        my_basket = self.filter(user_id=user_id).select_related("moment").values(
            "moment__id",
            "moment__publisher",
            "moment__cover_pic",
            "moment__num_comments",
            "moment__num_likes"
        )
        return my_basket


class Basket(models.Model):
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name="bucketed_moments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_moments")

    objects = BasketManager()

    def __str__(self):
        return str(self.id)


class SaveManager(models.Manager):
    def save_blog(self, user_id, data):
        blog_id = data.get("blog_id", None)
        if not blog_id:
            raise ValueError("blog_id is not provided")
        saved_instance, created = self.get_or_create(user_id=user_id, blog_id=blog_id)
        if not created:
            saved_instance.delete()
        return True

    def get_saved_blogs(self, user_id):
        blogs = self.filter(user_id=user_id)
        print("user_id", user_id)
        print("blogs", blogs)
        return blogs


class Save(models.Model):
    """
    for saving blogs
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_blogs")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="saves")

    objects = SaveManager()

    class Meta:
        verbose_name = "Blog Saves"

    def __str__(self):
        return self.user.username
