from django.contrib import admin
from .models import Conversation, Message


class ConversationAdmin(admin.ModelAdmin):
    autocomplete_fields = ["online"]
    
class MessageAdmin(admin.ModelAdmin):
    autocomplete_fields = ["from_user", "to_user"]

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)