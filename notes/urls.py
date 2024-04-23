from django.urls import path
from . import views

urlpatterns = [
    path("", views.NoteApiView.as_view())
]
