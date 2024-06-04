from django.urls import path
from . import views

urlpatterns = [
    path("blog/", views.ShareApiView.as_view(), name="share_blog")
]
