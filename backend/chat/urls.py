# chat/urls.py
from django.urls import path, include
from .api import ConversationViewSet
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("conversations", ConversationViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]