from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import MessageGroup
from .serializers import MessageSerializer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group = None
        self.sender = None
        self.receiver = None

    async def connect(self):
        try:
            print("hii")
            self.sender = self.scope["user"]
            print("user", self.sender)
            group_name = self.scope["url_route"]["kwargs"].get("group_name")
            self.group = await database_sync_to_async(MessageGroup.objects.get)(name=group_name)
            receiver_id = await database_sync_to_async(MessageGroup.objects.allocate_user)(self.sender.id, self.group)
            self.receiver = receiver_id
            if receiver_id:
                self.channel_layer.group_add(group_name, self.channel_name)
            else:
                return await self.close(code=404)
            print("connection established")
            await self.accept()

        except Exception as e:

            print("e", str(e))

    async def receive(self, text_data=None, bytes_data=None):
        print("message received", text_data)
        text_data = json.loads(text_data)

        # Validate incoming data using the serializer
        serializer = MessageSerializer(data=text_data)
        serializer.is_valid(raise_exception=True)

        # Create the message if validation passes
        message = await database_sync_to_async(serializer.create_message)(
            text_data, self.group, self.sender.id, self.receiver
        )
        print("message", message)
        # Send the message if creation is successful
        await self.send(json.dumps(message))

    async def disconnect(self, code):
        print("connection disclosed")
        await self.close(code)
