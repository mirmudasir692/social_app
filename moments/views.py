from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Moment, Leaf, Fruit
from .serializers import MomentSerializer, LeapSerializer, FruitSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator


class MomentApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, format=None):
        page = request.query_params.get("page", 1)
        try:
            moments = Moment.objects.get_moments(page=page, user=request.user)
            paginator = Paginator(moments, per_page=1)
            moment = paginator.get_page(page)
            print(moment)
            serializer = MomentSerializer(moment.object_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LeapApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


    @classmethod
    def post(cls, request):
        data = request.data
        user = request.user
        print("data", data)
        try:
            serializer = LeapSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                leap = Leaf.objects.like_moment(data, user_id=user.id)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print("error", str(e))
            return Response({"error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FruitApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):
        moment_id = request.query_params.get("moment_id", None)
        page = request.query_params.get("page", 1)
        fruits = Fruit.objects.get_fruits(moment_id)
        # paginator = Paginator(fruits, per_page=5)
        # fruits = paginator.get_page(page)
        print("F", fruits)
        serializer = FruitSerializer(fruits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def post(cls, request):
        data = request.data
        user = request.user
        print("data", data)
        try:
            serializer = FruitSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                fruit = serializer.create_fruit(data, user.id)
                newserializer = FruitSerializer(fruit)
                print("hii")
                return Response(newserializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        fruit_id = request.query_params.get("fid", None)
        user = request.user
        try:
            fruit = Fruit.objects.delete_fruit(fruit_id, user.id)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

