from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet


from .models import Conversation, Message

from .serializers import ConversationSerializer, MessageSerializer
from django.db.models import Q


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