from rest_framework import serializers
from .models import Recommendation
from datetime import datetime

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'

    def create(self, validated_data):
        obj = Recommendation.objects.get_or_create(from_user=validated_data.pop("from_user"), to_user=validated_data.pop("to_user"))[0]
        obj.recommended_on = datetime.now()
        obj.save()
        return obj