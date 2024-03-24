from rest_framework.views import APIView
from .serializers import BasketSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status


class BasketView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(cls, request):
        data = request.data
        user = request.user
        try:
            serializer = BasketSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                basket_item = serializer.add_to_basket(data, user.id)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
