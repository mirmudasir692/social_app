from django.urls import path
from . import views

urlpatterns = [
    path("chatbox/", views.ChatApiView.as_view()),
    path("message/", views.MessageChatApi.as_view()),
    path("list_groups/", views.UserAddFeatures.as_view())
]
