from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from . import serializers


class PostApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, format=None):
        user = request.user
        page_num = request.query_params.get("page_num", 1)
        posts, has_previous, has_next = Post.objects.get_posts(user.id, page_num)
        data = {
            "posts": posts,
            "has_previous": has_previous,
            "has_next": has_next
        }
        serializer = serializers.PostsWithPagination(data, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def post(cls, request, format=None):
        data = request.data
        print("data", data)
        user = request.user
        serializer = serializers.PostSerializer(data=data)
        post_instance = None
        if serializer.is_valid(raise_exception=True):
            post_instance = serializer.create_post(data, user.id)
        return Response(post_instance.data, status=status.HTTP_200_OK)


class PostLikeApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(cls, request, format=None):
        data = request.data
        user = request.user
        print("data", data)
        try:
            serializer = serializers.LikePostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                liked = serializer.create_like(data, user.id)
                print("liked", liked)
                return Response({"data": liked}, status=status.HTTP_200_OK)

            else:
                return Response({"data": False}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("error", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
