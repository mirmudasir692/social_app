from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import MessageGroup, Message
from .serializers import MessageGroupSerializer, MessageSerializer, ExtendedMessageSerializer, PartitionGrouSerializer


class ChatApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, format=None):
        user = request.user
        message_groups = MessageGroup.objects.get_groups(user.id)
        serializer = MessageGroupSerializer(message_groups, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageChatApi(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, format=None):
        group_id = request.query_params.get("group_id")
        messages = Message.objects.get_all_messages(group_id)
        print("grouping", group_id)
        # print("messages", messages)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAddFeatures(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, format=None):
        user = request.user
        groups = MessageGroup.objects.get_groups(user.id)
        serializer = PartitionGrouSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
