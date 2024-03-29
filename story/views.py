from rest_framework.views import APIView
from .serializers import StorySerializer, StoryLodgerSerializer, PaginatorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Story, StoryLodger
from django.core.paginator import Paginator


class StoryApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):
        user = request.user
        lodger_id = request.query_params.get("lodger_id", None)
        page_num = int(request.query_params.get("page_num", 1))
        try:
            stories = Story.objects.get_stories(user.id, lodger_id)
            paginator = Paginator(stories, per_page=1)
            page_stories = paginator.get_page(number=page_num)
            print("hello", page_stories.object_list)
            story_serializer = StorySerializer(page_stories, many=True)
            print("hii", story_serializer.data)
            serializer = PaginatorSerializer({
                "stories": story_serializer.data,
                "has_next": page_stories.has_next(),
                "has_previous": page_stories.has_previous(),
            })
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def post(cls, request):
        data = request.data
        user = request.user
        try:
            serializer = StorySerializer(data=data)
            print("data", data)
            if serializer.is_valid(raise_exception=True):
                story_item = serializer.create_story(data, user.id)
                item = StorySerializer(story_item)
            return Response(item.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StoryLodgerApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):
        user = request.user
        story_lodgers = StoryLodger.objects.story_exists(user.id)
        serializer = StoryLodgerSerializer(story_lodgers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
