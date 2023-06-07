from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .recommend import get_top_n_recommendations
from accounts.serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_recommendations(request, user_id=None, n=10):
    print("GETTING RECOMMENDATIONS")

    if not user_id:
        user_id = request.user.id

    recommendations = get_top_n_recommendations(user_id, n)

    
    # Convert the list of recommended user IDs to a JSON response
    response_data = {
        'recommendations': UserSerializer(recommendations, many=True).data
    }

    return JsonResponse(response_data)
