from django.urls import path
from . import views

urlpatterns = [
    path("watch/", views.MomentApiView.as_view(), name="watch"),
    path("leap/", views.LeapApiView.as_view(), name="leap")
]
