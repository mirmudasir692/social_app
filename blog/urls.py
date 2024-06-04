from django.urls import path
from . import views

urlpatterns = [
    path("", views.BlogApiView.as_view(), name="blog"),
    path("like/", views.LikeBlogApiView.as_view(), name="blog_like"),
    path("comment/", views.CommentApiView.as_view(), name="comment"),
    path("userops/", views.UserBlogApiView.as_view(), name="userops")
]
