from mailbox import Message
from chatsystem.models import Message as MessageModel
from rest_framework import serializers


class ShareSerializer(serializers.Serializer):
    blog_id = serializers.IntegerField(required=False)  # Required field for blog ID
    moment_id = serializers.IntegerField(required=False)
    group_name_list = serializers.ListField(
        child=serializers.CharField(),  # Specifies that it should be a list of strings
        required=True,  # Ensure it is a required field
        allow_empty=False  # Do not allow empty lists
    )

    def validate_blog_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Blog ID must be a positive integer.")
        return value

    def validate_group_name_list(self, value):
        for group_name in value:
            if not isinstance(group_name, str) or "$" not in group_name or "&" not in group_name:
                raise serializers.ValidationError(f"Invalid group name format: {group_name}")
        return value

    def handle_sharing(self,user_id, data):
        if data.get("blog_id"):
            return MessageModel.objects.share_blog(user_id, data)
        elif data.get("moment_id"):
            print("moment_id", data.get("moment_id"))
            return MessageModel.objects.share_moment(user_id, data)