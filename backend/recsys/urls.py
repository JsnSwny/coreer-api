from django.urls import path, include
from .views import get_recommendations, get_similarities
from rest_framework import routers
from .api import RecommendationViewSet

router = routers.DefaultRouter()
router.register("recommendations", RecommendationViewSet)


urlpatterns = [
    path('recommend/<int:user_id>/<int:n>', get_recommendations, name='get_recommendations'),
    path('api/', include(router.urls))
]