from django.contrib import admin
from .models import Conversation, Message

    
class MessageAdmin(admin.ModelAdmin):
    autocomplete_fields = ["from_user", "to_user"]

admin.site.register(Conversation)
admin.site.register(Message, MessageAdmin)