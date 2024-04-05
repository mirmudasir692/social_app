from rest_framework import serializers
from .models import User, Follow


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    @classmethod
    def check_user(cls, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = User.objects.authenticate_user(username=username, password=password)
        return user


class UserSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(format="%Y-%m-%d", required=False)
    password = serializers.CharField(write_only=True)
    followers_num = serializers.IntegerField(required=False)
    following_num = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['id', "username", "email", "mobile", "dob", "gender",
                  "password", "profile_pic", "name", "followers_num", "following_num"]

    def create(self, validated_data):
        username = validated_data.get("username", None)
        name = validated_data.get("name", None)
        mobile = validated_data.get("mobile", None)
        email = validated_data.get("email", None)
        gender = validated_data.get("gender", None)
        password = validated_data.get("password", None)
        dob = validated_data.get("dob", None)
        profile_pic = validated_data.get("profile_pic", None)
        user = User.objects.create_user(username=username, name=name, email=email, mobile=mobile, gender=gender, password=password, dob=dob, profile_pic=profile_pic)
        return user


class UserPartitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "verified", "profile_pic", "professional"]


class FollowSerializer(serializers.ModelSerializer):
    follower = UserPartitionSerializer(required=False)
    followed_user = UserPartitionSerializer(required=False)
    class Meta:
        model = Follow
        fields = ["follower", "followed_user"]

    @classmethod
    def follow_user(cls, follower_id, data):
        followed_user_id = data.get("followed_user_id", None)
        followed_item = Follow.objects.follow_user(follower_id, followed_user_id)
        return followed_item