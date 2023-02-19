from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .recommend import get_top_n_recommendations, similarities
from accounts.serializers import UserSerializer

@csrf_exempt
def get_recommendations(request, user_id):
    # Call the collaborative filtering function to get recommended users
    print("Getting recommendations...")
    recommendations = get_top_n_recommendations(user_id, n=10)

    
    # Convert the list of recommended user IDs to a JSON response
    response_data = {
        'recommendations': UserSerializer(recommendations, many=True).data
    }

    return JsonResponse(response_data)


@csrf_exempt
def get_similarities(request, user_id):
    # Call the collaborative filtering function to get recommended users
    print("Getting recommendations...")
    recommendations = similarities(user_id)
    
    # Convert the list of recommended user IDs to a JSON response
    response_data = {
        'recommendations': UserSerializer(recommendations, many=True).data
    }
    return JsonResponse(response_data)
