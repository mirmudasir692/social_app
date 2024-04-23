from rest_framework import serializers
from .models import Message, MessageGroup
from moments.serializers import MomentSerializer
from blog.serializers import BlogSerializer
from accounts.serializers import UserPartitionSerializer
from utils.chatsystem import decrypt_message


class MessageGroupSerializer(serializers.ModelSerializer):
    receiver = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = MessageGroup
        fields = ["name", "receiver", "last_message"]

    def get_receiver(self, obj):
        request = self.context.get("request")
        if obj.user1.id == request.user.id:
            receiver = UserPartitionSerializer(obj.user2)
            return receiver.data
        else:
            receiver = UserPartitionSerializer(obj.user1)
            return receiver.data

    def get_last_message(self, obj):
        request = self.context.get("request")
        last_message = obj.group_messages.last()
        # last_message = Message.objects.get_last_message(obj, request.user.id)
        print("message", last_message)
        print("last_message", last_message)
        if last_message:
            # last_message.message = decrypt_message(last_message.message)
            serialized_last_message = MessageSerializer(last_message).data
            return serialized_last_message
        else:
            return None


class MessageSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=False)
    moment = MomentSerializer(required=False)
    blog = BlogSerializer(required=False)
    file = serializers.FileField(required=False)
    sender = UserPartitionSerializer(required=False)
    receiver = UserPartitionSerializer(required=False)
    show_to_user = serializers.BooleanField(required=False)

    class Meta:
        model = Message
        fields = ["id", "message", "moment", "blog", "timestamp", "file", "sender", "receiver", "show_to_user"]

    @classmethod
    def create_message(cls, data, group, sender_id, receiver_id):
        message = Message.objects.save_message(data, group, sender_id, receiver_id)
        serializer = cls(message)
        return serializer.data


class ExtendedMessageSerializer(serializers.Serializer):
    messages = MessageSerializer(many=True)
    receiver = UserPartitionSerializer()
