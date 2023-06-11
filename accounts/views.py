from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.serializers import UserSerializer, LanguageSerializer
from .models import Language, CustomUser, Follow
from django.db.models import Count
import redis
from scipy.sparse import coo_matrix, csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer#


@csrf_exempt
def get_popular_languages(request):
    most_common_languages = Language.objects.annotate(num_users=Count('customuser')).order_by('-num_users')[0:50]
    response_data = {
        'languages': LanguageSerializer(most_common_languages, many=True).data
    }
    return JsonResponse(response_data)

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "localhost:8000/login"
    client_class = OAuth2Client

import requests
import json

@csrf_exempt
def exchange_code_for_access_token(request):
    data = json.loads(request.body.decode())
    code = data["code"]

    # Make a POST request to the GitHub OAuth access token endpoint
    data = {
        'client_id': '4710f43b56ca1572e2a8',
        'client_secret': 'a265125f9ee537c3e0665fdecb8b7cc32af0d156',
        'code': code
    }

    print(data)

    response = requests.post('https://github.com/login/oauth/access_token', data=data, headers={'Accept': 'application/json'})

    if response.ok:
        access_token = response.json().get('access_token')
        return JsonResponse({'access_token': access_token})
    else:
        return JsonResponse({'error': 'Failed to exchange code for access token'}, status=500)