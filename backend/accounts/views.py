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
