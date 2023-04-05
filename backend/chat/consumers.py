import json

from asgiref.sync import async_to_sync
from .models import Conversation, Message
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer

User = get_user_model()

class ChatConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None

    def get_receiver(self):
        userIds = self.conversation_name.split("__")
        for id in userIds:
            print(id)
            print(self.user.id)
            print(self)
            if id != self.user.id:
                return User.objects.get(id=id)

    def connect(self):
        self.user = self.scope["user"]
        print("Connecting")
        print(self.scope)
        print(self.scope['user'])
        print("user")
        self.conversation_name = self.scope["url_route"]["kwargs"]["room_name"]
        print(self.conversation_name)
        self.conversation, created = Conversation.objects.get_or_create(name=self.conversation_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        

        self.accept()

        messages = self.conversation.messages.all().order_by("timestamp")[0:50]
        print(messages)
        messages_ser = MessageSerializer(messages, many=True).data

        self.send_json({
            "type": "message_history",
            "messages": messages_ser,
        })

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.conversation_name,
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            message = Message.objects.create(
                from_user=self.user,
                to_user=self.get_receiver(),
                content=content["message"],
                conversation=self.conversation
            )

            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "chat_message_echo",
                    "message": MessageSerializer(message, many=False).data,
                },
            )
        return super().receive_json(content, **kwargs)

    def chat_message_echo(self, event):
        print(event)
        self.send_json(event)