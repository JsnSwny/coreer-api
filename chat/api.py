from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet


from .models import Conversation, Message

from .serializers import ConversationSerializer, MessageSerializer
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status


class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()
    lookup_field = "name"

    def get_queryset(self):
        queryset = Conversation.objects.filter(
            name__contains=self.request.user.id
        )

        return queryset

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}
    
class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.none()

    def get_queryset(self):
        queryset = Message.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user.id) 
        )

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Check if the most recent message was more than an hour ago
        last_message = Message.objects.filter(to_user=self.request.user).order_by('-timestamp').first()
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
                    [self.to_user.email],  # Replace with the recipient's email address
                    fail_silently=False,
                )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)