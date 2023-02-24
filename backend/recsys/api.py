from .serializers import RecommendationSerializer
from .models import Recommendation
from rest_framework import viewsets

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    def get_queryset(self):
        return Recommendation.objects.all()
