from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name="login_user"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("register/", views.RegisterUserApiView.as_view(), name="register_user")
]