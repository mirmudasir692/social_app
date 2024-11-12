from rest_framework.views import APIView
from .serializers import BasketSerializer, SaveBlogSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import Basket


class BasketView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):
        user = request.user
        my_basket = Basket.objects.get_my_basket(user.id)
        serializer = BasketSerializer(my_basket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def post(cls, request):
        data = request.data
        user = request.user
        try:
            serializer = BasketSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                basket_item = serializer.add_to_basket(data, user.id)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SaveBlogApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):
        user = request.user
        serializer = SaveBlogSerializer.get_blogs(user.id)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def post(cls, request, format=None):
        data = request.data
        user = request.user
        serializer = SaveBlogSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save_blog(user.id, data)
                return Response(status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


