from django.urls import path
from .import views

urlpatterns = [
    path("basket/", views.BasketView.as_view(), name="basket")
]