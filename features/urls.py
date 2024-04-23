from django.urls import path
from .import views

urlpatterns = [
    path("basket/", views.BasketView.as_view(), name="basket"),
    path("blog/", views.SaveBlogApiView.as_view())
]
