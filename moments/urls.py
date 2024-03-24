from django.urls import path
from . import views

urlpatterns = [
    path("watch/", views.MomentApiView.as_view(), name="watch"),
    path("leaf/", views.LeapApiView.as_view(), name="leap"),
    path("fruit/", views.FruitApiView.as_view(), name="fruit"),
]
