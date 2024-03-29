from rest_framework import serializers

from chat.models import Message, Conversation
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from accounts.models import CustomUser


class MessageSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    from_user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CustomUser.objects.all(), source="from_user")
    to_user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CustomUser.objects.all(), source="to_user")

    conversation = serializers.SerializerMethodField()
    conversation_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Conversation.objects.all(), source="conversation")


    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "from_user",
            "to_user",
            "to_user_id",
            "from_user_id",
            "conversation_id",
            "content",
            "timestamp",
            "read",
        )

    def get_conversation(self, obj):
        return str(obj.conversation.id)

User = get_user_model()


from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    def save(self, request):
        user = super().save(request)
        user.emailaddress_set.update(verified=True)
        return user

class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "name", "other_user", "last_message")

    def get_last_message(self, obj):
        messages = obj.messages.all().order_by("-timestamp")
        if not messages.exists():
            return None
        message = messages[0]
        return MessageSerializer(message).data

    def get_other_user(self, obj):
        ids = obj.name.split("__")
        
        for id in ids:
            if int(id) != int(self.context["user"].id):
                other_user = User.objects.get(id=id)
                return UserSerializer(other_user).data