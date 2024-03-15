from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers
from utils.accounts import GenerateTokens


class LoginUserView(APIView):
    def post(self, request):
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
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterUserApiView(APIView):
    def post(self, request):
        data = request.data
        try:
            serializer = serializers.RegisterUserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                """
                create user instance, save it and generate pair of tokens(refresh token and access token)
                """
                data = GenerateTokens.get_tokens(user)
                return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"data": str(e)}, status=status.HTTP_400_BAD_REQUEST)