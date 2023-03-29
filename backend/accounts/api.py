from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import ProfilesSerializer, UserSerializer, LoginSerializer, RegisterSerializer, FollowSerializer, InterestSerializer
from .models import CustomUser, Follow, Interest
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.contrib.auth import login
import redis
from scipy.sparse import csr_matrix
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        r = redis.Redis(host='localhost', port=6379, db=0)

        user_ids = list(CustomUser.objects.values_list("id", flat=True).order_by("id"))
        id_dict = dict(zip(user_ids, range(len(user_ids))))
        following = Follow.objects.values_list("follower__id", "following__id")

        
        row = []
        col = []
        data = []

        for i in following:
            row.append(id_dict[i[0]])
            col.append(id_dict[i[1]])
            data.append(1)

        sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_ids), len(user_ids)), dtype=np.int32)

        r.set('csr_matrix_data', sparse_matrix.data.tobytes())
        r.set('csr_matrix_indices', sparse_matrix.indices.tobytes())
        r.set('csr_matrix_indptr', sparse_matrix.indptr.tobytes())
        r.set('csr_matrix_shape', np.array(sparse_matrix.shape, dtype=np.int32).tobytes())

        vec = TfidfVectorizer(strip_accents="unicode", stop_words="english", min_df=3)
        user_bios = list(CustomUser.objects.values_list("tfidf_input", flat=True).order_by("id"))
        tfidf_matrix = vec.fit_transform(user_bios)

        r.set('tfidf_matrix_data', tfidf_matrix.data.tobytes())
        r.set('tfidf_matrix_indices', tfidf_matrix.indices.tobytes())
        r.set('tfidf_matrix_indptr', tfidf_matrix.indptr.tobytes())
        r.set('tfidf_matrix_shape', np.array(tfidf_matrix.shape, dtype=np.int32).tobytes())

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Get User API

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# # Get User API

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UpdateUserSerializer

#     def get_queryset(self):
#         return self.request.user

from rest_framework import filters
# from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend


class UpdateUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    search_fields = ['first_name', 'last_name']

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'id': ["in", "exact"], # note the 'in' field
    }
    

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_object(self):
        obj = get_object_or_404(CustomUser.objects.filter(id=self.kwargs["pk"]))
        return obj

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = request.user
        clean_input = ""
        if user.bio:
            clean_input += user.bio
        if len(user.languages.all()) > 0:
            for language in user.languages.all():
                clean_input += f" {language.name}"
        if len(user.interests.all()) > 0:
            for interest in user.interests.all():
                clean_input += f" {interest.name}"

        user.tfidf_input = clean_input
        user.save()

        r = redis.Redis(host='localhost', port=6379, db=0)

        user_ids = list(CustomUser.objects.values_list("id", flat=True).order_by("id"))
        id_dict = dict(zip(user_ids, range(len(user_ids))))
        following = Follow.objects.values_list("follower__id", "following__id")

        
        row = []
        col = []
        data = []

        for i in following:
            row.append(id_dict[i[0]])
            col.append(id_dict[i[1]])
            data.append(1)

        sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_ids), len(user_ids)), dtype=np.int32)

        r.set('csr_matrix_data', sparse_matrix.data.tobytes())
        r.set('csr_matrix_indices', sparse_matrix.indices.tobytes())
        r.set('csr_matrix_indptr', sparse_matrix.indptr.tobytes())
        r.set('csr_matrix_shape', np.array(sparse_matrix.shape, dtype=np.int32).tobytes())

        vec = TfidfVectorizer(strip_accents="unicode", stop_words="english", min_df=3)
        user_bios = list(CustomUser.objects.values_list("tfidf_input", flat=True).order_by("id"))
        tfidf_matrix = vec.fit_transform(user_bios)

        r.set('tfidf_matrix_data', tfidf_matrix.data.tobytes())
        r.set('tfidf_matrix_indices', tfidf_matrix.indices.tobytes())
        r.set('tfidf_matrix_indptr', tfidf_matrix.indptr.tobytes())
        r.set('tfidf_matrix_shape', np.array(tfidf_matrix.shape, dtype=np.int32).tobytes())

        return Response(serializer.data)

# Get User API

class ProfilesViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfilesSerializer

    def get_queryset(self):
        print("Getting all users")
        return CustomUser.objects.all()

    def get_object(self):
        obj = get_object_or_404(CustomUser.objects.filter(id=self.kwargs["pk"]))
        return obj

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        print("Follow created")
        
        response = super().create(request, *args, **kwargs)

        r = redis.Redis(host='localhost', port=6379, db=0)
   
        csr_matrix_data = np.frombuffer(r.get('csr_matrix_data'), dtype=np.int32)
        csr_matrix_indices = np.frombuffer(r.get('csr_matrix_indices'), dtype=np.int32)
        csr_matrix_indptr = np.frombuffer(r.get('csr_matrix_indptr'), dtype=np.int32)
        csr_matrix_shape = np.frombuffer(r.get('csr_matrix_shape'), dtype=np.int32)
        sparse_matrix = csr_matrix((csr_matrix_data, csr_matrix_indices, csr_matrix_indptr), shape=tuple(csr_matrix_shape))

        user_ids = list(CustomUser.objects.values_list("id", flat=True).order_by("id"))
        id_dict = dict(zip(user_ids, range(len(user_ids))))

        sparse_matrix_copy = sparse_matrix.copy() 

        sparse_matrix_copy[id_dict[response.data["follower"]], id_dict[response.data["following"]]] = 1 
        
        
        r.set('csr_matrix_data', sparse_matrix_copy.data.tobytes())
        r.set('csr_matrix_indices', sparse_matrix_copy.indices.tobytes())
        r.set('csr_matrix_indptr', sparse_matrix_copy.indptr.tobytes())
        r.set('csr_matrix_shape', np.array(sparse_matrix_copy.shape, dtype=np.int32).tobytes())
        
        return response

    def get_queryset(self):
        return Follow.objects.all()
    
class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

    def get_queryset(self):
        return Interest.objects.all()