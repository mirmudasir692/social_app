from django.urls import path
from . import views

urlpatterns = [
    path("", views.StoryApiView.as_view(), name="story"),
    path("lodger/", views.StoryLodgerApiView.as_view(), name="storylodger")
]
