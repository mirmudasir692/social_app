from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name="login_user"),
    path("refresh/", views.RefreshTokenApiView.as_view(), name="refresh_token"),
    path("register/", views.RegisterUserApiView.as_view(), name="register_user"),
    path("myaccount/", views.AdditionalUserFeatures.as_view(), name="additional_features"),
    path("follow/", views.FollowApiView.as_view(), name="follow")
]