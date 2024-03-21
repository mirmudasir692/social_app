from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Moment, Leap
from .serializers import MomentSerializer, LeapSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator


class MomentApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        page = request.query_params.get("page", 1)
        try:
            moments = Moment.objects.get_moments(page=page, user=request.user)
            paginator = Paginator(moments, per_page=1)
            moment = paginator.get_page(page)
            print(moment)
            serializer = MomentSerializer(moment.object_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LeapApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        user = request.user
        print("data", data)
        try:
            serializer = LeapSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                leap = Leap.objects.like_moment(data, user_id=user.id)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)

