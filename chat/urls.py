# chat/urls.py
from django.urls import path, include
from .api import ConversationViewSet, MessageViewSet
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("conversations", ConversationViewSet)
router.register("messages", MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]