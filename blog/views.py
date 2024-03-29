from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.core.paginator import Paginator


class BlogApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, format=None):
        user = request.user
        page_num = request.query_params.get("page_num", 1)
        blogs = Blog.objects.get_blogs(user.id)
        paginator = Paginator(blogs, per_page=5)
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
