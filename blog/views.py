from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog, Like, Comment
from django.core.paginator import Paginator


class BlogApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, format=None):
        user = request.user
        page_num = request.query_params.get("page_num", 1)
        blogs = Blog.objects.get_blogs(user.id)
        paginator = Paginator(blogs, per_page=4)
        page_blogs = paginator.get_page(page_num)
        serializer = BlogSerializer(page_blogs.object_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def post(cls, request, format=None):
        data = request.data
        user = request.user
        try:
            serializer = BlogSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                blog = serializer.create_blog(data, user.id)
                blog_serializer = BlogSerializer(blog)
                return Response(blog_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("e", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def delete(cls, request, format=None):
        user = request.user
        blog_id = request.query_params.get("blog_id", None)
        try:
            deleted = Blog.objects.delete_blog(blog_id, user.id)
            if deleted:
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LikeBlogApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):
        user = request.user
        blog_id = request.query_params.get("blog_id", None)
        liked = Like.objects.like_blog(user_id=user.id, blog_id=blog_id)
        return Response({"liked":liked}, status=status.HTTP_200_OK)


class CommentApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):
        blog_id = request.query_params.get("blog_id", None)
        page_num = request.query_params.get("page_num", 1)
        comments = Comment.objects.get_comments(blog_id)
        paginator = Paginator(comments, per_page=1)
        comments_for_page = paginator.get_page(number=page_num)
        has_previous = comments_for_page.has_previous()
        has_next = comments_for_page.has_next()
        serializer = CommentSerializer(comments_for_page, many=True)
        return Response({
            'comments': serializer.data,
            'has_previous': has_previous,
            'has_next': has_next},
            status=status.HTTP_200_OK)

    @classmethod
    def post(cls, request):
        data = request.data
        user = request.user
        serializer = CommentSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                comment = serializer.add_comment(data, user.id)
                comment_serializer = CommentSerializer(comment)
                return Response(comment_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("e", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserBlogApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, format=None):
        user = request.user
        try:
            blogs = Blog.objects.get_user_blogs(user.id)
            serializer = BlogSerializer(blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("e", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

