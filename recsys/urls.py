from django.urls import path, include
from .views import get_recommendations
from rest_framework import routers
from .api import RecommendationViewSet

router = routers.DefaultRouter()
router.register("recommendations", RecommendationViewSet)


urlpatterns = [
    path('recommend/<int:n>', get_recommendations, name='get_recommendations'),
    path('recommend/<int:n>/<int:user_id>', get_recommendations, name='get_recommendations'),
    path('api/', include(router.urls))
]