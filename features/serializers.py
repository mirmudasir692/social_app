from rest_framework import serializers
from .models import Basket
from accounts.serializers import UserPartitionSerializer
from moments.serializers import MomentSerializer


class BasketSerializer(serializers.ModelSerializer):
    moment = MomentSerializer(required=False)
    user = UserPartitionSerializer(write_only=True, required=False)

    class Meta:
        model = Basket
        fields = ["id", "moment", "user"]

    @classmethod
    def add_to_basket(cls, validated_data, user_id):
        moment_id = validated_data.get("moment_id", None)
        basket_item = Basket.objects.add_to_basket(moment_id, user_id)
        return basket_item