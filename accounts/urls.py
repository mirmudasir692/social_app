from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name="login_user"),
    path("csrf/", views.get_custom_csrf, name="get_csrf"),
    path("refresh/", views.RefreshTokenApiView.as_view(), name="refresh_token"),
    path("register/", views.RegisterUserApiView.as_view(), name="register_user"),
    path("myaccount/", views.AdditionalUserFeatures.as_view(), name="additional_features"),
    path("follow/", views.FollowApiView.as_view(), name="follow"),
    path("friend_profile/", views.ProfileApiView.as_view(), name="friend_profile"),
    path("my_followers/", views.FollowerFeatures.as_view(), name="my_followings"),
    path("search/", views.SearchUser.as_view()),
    path("auth/", include("allauth.urls")),  # This should be first among auth URLs
    path("google/callback/", views.GoogleLoginCallback.as_view(), name="google_callback"),  # Fixed URL pattern
    path("google/validate-token/", views.GoogleToken.as_view(), name="validate_token")  # More REST-like URL
]