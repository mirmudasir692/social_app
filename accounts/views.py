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
from time import sleep


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
                sleep(5)
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
        user = request.user
        followers_list = Follow.objects.get_all_followers(user.id)
        serializer = serializers.UserPartitionSerializer(followers_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
