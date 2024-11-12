from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import NoteSerializer
from .models import Note


class NoteApiView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):
        my_note = request.query_params.get("my_note", False)
        if my_note:
            note = Note.objects.get(user_id=request.user.id)
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)

        notes = Note.objects.get_notes(request.user.id)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def post(cls, request):
        data = request.data
        serializer = NoteSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                note_instance = serializer.create_note(data, request.user.id)
                return Response(note_instance.data, status=status.HTTP_200_OK)
        except ValueError as e:
            print("error", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def patch(cls, request):
        data = request.data
        serializer = NoteSerializer(data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            note = serializer.update_note(data, request.user.id)
            print("note", note.data)
            return Response(note.data, status=status.HTTP_200_OK)


