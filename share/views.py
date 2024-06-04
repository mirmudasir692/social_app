from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from chatsystem.models import Message
from .serializer import ShareSerializer
from rest_framework.response import Response
from rest_framework import status


class ShareApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(cls, request):
        user = request.user
        data = request.data
        print("data", data)
        try:
            serializer = ShareSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                Message.objects.share_blog(user.id, data)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

