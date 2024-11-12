from sys import platform

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers
from utils.accounts import GenerateTokens
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User, Follow
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.exceptions import ValidationError
from urllib.parse import unquote
from google.oauth2 import id_token
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import  AllowAny
import requests
from django.core.files.base import ContentFile


from .serializers import UserPartitionSerializer, ExtendedUserSerializer, UserSerializer

from allauth.socialaccount.models import SocialToken, SocialAccount


@api_view(["GET"])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_custom_csrf(request):
    return Response({"message":"CSRF token set"})

class LoginUserView(APIView):
    @classmethod
    def post(cls, request):
        data = request.data
        print(data)
        try:
            serializer = serializers.LoginUserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.check_user(data)
                data = GenerateTokens.get_tokens(user)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            print(e)
            return Response(str(e))
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class RegisterUserApiView(APIView):
    @classmethod
    def post(cls, request):
        data = request.data
        print("data", data)
        try:
            serializer = serializers.UserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                """
                create user instance, save it and generate pair of tokens(refresh token and access token)
                """
                data = GenerateTokens.get_tokens(user)
                return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            print("e", str(e))
            return Response({"data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("e", str(e))
            return Response({"data": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdditionalUserFeatures(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):
        user = request.user
        """this allows user to see their profile"""
        try:
            user = User.objects.get(id=user.id)
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        data = request.data
        user = request.user
        try:
            serializer = UserSerializer(data, partial=True)
            user = serializer.update_user(user.id, data)
            return Response(user, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenApiView(TokenRefreshView):
    @classmethod
    def post(cls, request, *args, **kwargs):
        data = request.data
        refresh_token = data.get("refresh_token", None)
        print(refresh_token)
        if refresh_token:
            """
            check whether refresh token valid then refresh token 
            """
            refresh_token = RefreshToken(token=refresh_token)
            data = {
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token)
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FollowApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(cls, request):
        data = request.data
        user = request.user
        serializer = serializers.FollowSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                followed_item = serializer.follow_user(user.id, data)
                if followed_item:
                    return Response(status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, format=None):
        user_id = request.query_params.get("frnd_id", None)
        friend_profile = User.objects.get_friend_profile(user_id)
        serializer = serializers.FriendSerializer(friend_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowerFeatures(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, format=None):
        """
        to get the follower list
        :param request:
        :param format:
        :return:
        """
        followers = request.query_params.get("followers", True)
        followers = True if followers == "true" else False
        user = request.user
        print("followers", followers)
        if followers:
            followers_list = Follow.objects.get_all_followers(user.id)
            serializer = serializers.ExtendedUserSerializer(followers_list, many=True)
        else:
            following_list = Follow.objects.get_following_list(user.id)
            serializer = serializers.ExtendedUserSerializer(following_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchUser(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        username_param = request.query_params.get("param", "")
        username = unquote(username_param).strip('"')
        user = request.user
        try:
            users = User.objects.search_users(username, user.id)
            serializer = serializers.ExtendedUserSerializer(users, many=True)
            print("data", serializer.data)
            return Response({"data": serializer.data})
        except Exception as e:
            print("e", e)
            return Response({"error": str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class GoogleLoginCallback(APIView):

    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response({"detail": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the access token and get user info
            user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
            response = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"})

            if response.status_code != 200:
                return Response({"detail": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)

            user_info = response.json()
            print("user_info", user_info)
            google_user_id = user_info.get("sub")
            email = user_info.get("email")
            username = email.split("@")[0]
            profile_pic_url = user_info["picture"]

            # Download the profile picture
            profile_pic_response = requests.get(profile_pic_url)
            if profile_pic_response.status_code != 200:
                return Response({"detail": "Failed to download profile picture"}, status=status.HTTP_400_BAD_REQUEST)

            user, created = User.objects.get_or_create(identifier=google_user_id, username=username)

            # Save the profile picture to the user model
            if created or not user.profile_pic:  # Only set if the user is newly created or the profile pic is not already set
                image_name = f"{google_user_id}_profile_pic.jpg"  # Generate a unique name for the image
                user.profile_pic.save(image_name, ContentFile(profile_pic_response.content))  # Save the image

            data = GenerateTokens.get_tokens(user)
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@method_decorator(csrf_exempt, name="dispatch")
class GoogleToken(APIView):
    def post(self, request, format=None):
        try:
            # Get the access token from the request
            google_access_token = request.data.get("token")
            if not google_access_token:
                return Response(
                    {"detail": "Access Token is missing"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify the Google token using Google’s OAuth2 library
            idinfo = id_token.verify_oauth2_token(
                google_access_token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID  # Ensure this is set in your Django settings
            )

            # Extract user details from the token
            google_user_id = idinfo.get("sub")
            email = idinfo.get("email")

            # Retrieve or create a new user based on the email from the Google token
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": email.split("@")[0], "google_id": google_user_id}
            )

            # Generate JWT tokens (access and refresh tokens)
            refresh = RefreshToken.for_user(user)
            data = {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }

            return Response(data, status=status.HTTP_200_OK)

        except ValueError:
            # If the token verification fails
            return Response(
                {"detail": "Invalid Google token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )