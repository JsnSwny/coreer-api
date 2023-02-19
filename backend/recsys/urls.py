from django.urls import path
from .views import get_recommendations, get_similarities

urlpatterns = [
    path('<int:user_id>/', get_recommendations, name='get_recommendations'),
    path('content/<int:user_id>/', get_similarities, name='get_similarities'),
]