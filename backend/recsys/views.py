from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .recommend import get_top_n_recommendations
from accounts.serializers import UserSerializer

@csrf_exempt
def get_recommendations(request, user_id, n=10):
    # Call the collaborative filtering function to get recommended users

    print("USER")
    print(request.user)
    print("Getting recommendations...")
    recommendations = get_top_n_recommendations(user_id, n)

    
    # Convert the list of recommended user IDs to a JSON response
    response_data = {
        'recommendations': UserSerializer(recommendations, many=True).data
    }

    return JsonResponse(response_data)
