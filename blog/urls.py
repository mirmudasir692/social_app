from django.urls import path
from . import views

urlpatterns = [
    path("", views.BlogApiView.as_view(), name="blog")
]