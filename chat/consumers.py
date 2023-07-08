import json

from asgiref.sync import async_to_sync
from .models import Conversation, Message
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer, ConversationSerializer
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta

User = get_user_model()

class NotificationConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return

        self.accept()

        # private notification group
        self.notification_group_name = self.user.username + "__notifications"
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )

        # unread_count = Message.objects.filter(to_user=self.user, read=False).count()
        # self.send_json(
        #     {
        #         "type": "unread_count",
        #         "unread_count": unread_count,
        #     }
        # )

    def read_messages(self, event):
        print("Notification: new_message_notification")
        self.send_json(event)

    def new_message_notification(self, event):
        print("Notification: new_message_notification")
        self.send_json(event)

class ChatConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None

    def get_receiver(self):
        userIds = self.conversation_name.split("__")
        print(userIds)
        for id in userIds:
            print(id)
            print(self.user.id)
            if int(id) != int(self.user.id):
                return User.objects.get(id=id)

    def connect(self):
        self.user = self.scope["user"]
        self.conversation_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.conversation, created = Conversation.objects.get_or_create(name=self.conversation_name)
        

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        

        self.accept()

        messages = self.conversation.messages.all().order_by("timestamp")[0:50]
        messages_ser = MessageSerializer(messages, many=True).data

        self.send_json({
            "type": "message_history",
            "messages": messages_ser,
            "conversation": ConversationSerializer(self.conversation, context={"user": self.scope["user"]}).data
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
            print("SENDING MESSAGE")
            message = Message.objects.create(
                from_user=self.user,
                to_user=self.get_receiver(),
                content=content["message"],
                conversation=self.conversation
            )

            last_message = Message.objects.filter(to_user=self.get_receiver()).order_by('-timestamp').first()
            if last_message and timezone.now() - last_message.timestamp > timedelta(hours=1):
                # Send email notification to the 'to_user'
                send_mail(
                    'New Message Notification',
                    'You have received a new message.',
                    'coreer.info@gmail.com',  # Replace with the sender's email address
                    [last_message.to_user.email],  # Replace with the recipient's email address
                    fail_silently=False,
                )
            else:
                if not last_message:
                    send_mail(
                        'New Message Notification',
                        'You have received your first message on Coreer.',
                        'coreer.info@gmail.com',  # Replace with the sender's email address
                        [self.get_receiver().to_user.email],  # Replace with the recipient's email address
                        fail_silently=False,
                    )

                async_to_sync(self.channel_layer.group_send)(
                    self.conversation_name,
                    {
                        "type": "chat_message_echo",
                        "message": MessageSerializer(message, many=False).data,
                    },
                )

            notification_group_name = self.get_receiver().username + "__notifications"
            print("Sender: " + self.user.username)
            print("Receiver: " + self.get_receiver().username)
            print("Sending to " + self.get_receiver().username + "__notifications")
            async_to_sync(self.channel_layer.group_send)(
                notification_group_name,
                {
                    "type": "new_message_notification",
                    "name": self.user.first_name,
                    "message": MessageSerializer(message).data,
                    "conversation": ConversationSerializer(self.conversation, context={"user": self.get_receiver()}).data
                },
            )

            return super().receive_json(content, **kwargs)
        
        if message_type == "read_messages":
            messages_to_me = self.conversation.messages.filter(to_user=self.user)
            messages_to_me.update(read=True)

            print("CHAT: Read Messages")

            # Update the unread message count
            # unread_count = Message.objects.filter(to_user=self.user, read=False).count()
            async_to_sync(self.channel_layer.group_send)(
                self.user.username + "__notifications",
                {
                    "type": "read_messages",
                    "conversation": ConversationSerializer(self.conversation, context={"user": self.get_receiver()}).data
                },
            )

    def chat_message_echo(self, event):
        self.send_json(event)

    

    def new_message_notification(self, event):
        print("CHAT: new_message_notification")
        self.send_json(event)