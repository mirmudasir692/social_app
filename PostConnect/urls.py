from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostApiView.as_view()),
    path("like/", views.PostLikeApiView.as_view())
]
