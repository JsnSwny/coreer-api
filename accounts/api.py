from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import ProfilesSerializer, UserSerializer, LoginSerializer, RegisterSerializer, FollowSerializer, InterestSerializer, ProjectSerializer, SchoolSerializer, EducationSerializer, WorkExperienceSerializer, QuestionSerializer, UserAnswerSerializer, CareerLevelSerializer
from .models import CustomUser, Follow, Interest, Project, School, Education, WorkExperience, Question, UserAnswer, CareerLevel
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.contrib.auth import authenticate, login
import redis
from scipy.sparse import csr_matrix
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'perPage'
    max_page_size = 100


class UpdateUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    search_fields = ['first_name', 'last_name', 'job', 'location', 'bio', 'languages__name']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'id': ["in", "exact"]
    }

    def get_unique_username(self, first_name, last_name):
        base_username = f"{first_name.lower()}-{last_name.lower()}"
        username = base_username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}-{counter}"
            counter += 1
        return username


    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()



        user = request.user

        user.username = self.get_unique_username(user.first_name, user.last_name)

        if len(user.languages.all()) > 0:
            clean_input = ""
            if user.bio:
                clean_input += user.bio

            if len(user.interests.all()) > 0:
                for interest in user.interests.all():
                    clean_input += f"{interest.name} "

            if len(user.languages.all()) > 0:
                for language in user.languages.all():
                    clean_input += f"[lang_{language.name}] "
            
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

            vec = TfidfVectorizer(strip_accents="unicode", stop_words="english")
            user_bios = list(CustomUser.objects.values_list("tfidf_input", flat=True).order_by("id"))
            tfidf_matrix = vec.fit_transform(user_bios)

            r.set('tfidf_matrix_data', tfidf_matrix.data.tobytes())
            r.set('tfidf_matrix_indices', tfidf_matrix.indices.tobytes())
            r.set('tfidf_matrix_indptr', tfidf_matrix.indptr.tobytes())
            r.set('tfidf_matrix_shape', np.array(tfidf_matrix.shape, dtype=np.int32).tobytes())

        return Response(serializer.data)

# Get User API

class RetrieveProfile(generics.RetrieveAPIView):
    serializer_class = ProfilesSerializer

    def get_object(self):
        username = self.kwargs['username']
        obj = get_object_or_404(CustomUser.objects.filter(username=username))
        return obj
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
    
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
    
class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer


class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

class CareerLevelList(generics.ListAPIView):
    serializer_class = CareerLevelSerializer
    queryset = CareerLevel.objects.all()


    

class SchoolPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'perPage'
    max_page_size = 100

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    pagination_class = SchoolPagination

    search_fields = ['name']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def get_queryset(self):
        return School.objects.all()
    
class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def get_queryset(self):
        return Education.objects.all()
    
class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer

    def get_queryset(self):
        return WorkExperience.objects.all()
    

class FollowAPIView(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['follower__id']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['followed_on']

    def get_queryset(self):
        print("Get me some follows")
        return Follow.objects.filter(follower=self.request.user)

    def create(self, request, *args, **kwargs):
        following_id = request.data.get('following_id')
        print(f"POST: Following id is: {following_id}")
        if not following_id:
            return Response({'error': 'following_id is required'}, status=400)
        

        try:
            following = CustomUser.objects.get(id=following_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following)
        r = redis.Redis(host='localhost', port=6379, db=0)

        if r.exists('csr_matrix_data'):
            print("Exists")
        else:
            user_objects = CustomUser.objects.all().order_by("id")
            user_ids = list(user_objects.values_list("id", flat=True))
            id_dict = dict(zip(user_ids, range(len(user_ids))))
            
            following = Follow.objects.all().values_list("follower__id", "following__id")
            
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

            print("MATRIX DATA CREATED")
   
        csr_matrix_data = np.frombuffer(r.get('csr_matrix_data'), dtype=np.int32)
        csr_matrix_indices = np.frombuffer(r.get('csr_matrix_indices'), dtype=np.int32)
        csr_matrix_indptr = np.frombuffer(r.get('csr_matrix_indptr'), dtype=np.int32)
        csr_matrix_shape = np.frombuffer(r.get('csr_matrix_shape'), dtype=np.int32)
        sparse_matrix = csr_matrix((csr_matrix_data, csr_matrix_indices, csr_matrix_indptr), shape=tuple(csr_matrix_shape))

        user_ids = list(CustomUser.objects.values_list("id", flat=True).order_by("id"))
        id_dict = dict(zip(user_ids, range(len(user_ids))))

        sparse_matrix_copy = sparse_matrix.copy() 

        sparse_matrix_copy[id_dict[request.user.id], id_dict[following_id]] = 1
        
        
        r.set('csr_matrix_data', sparse_matrix_copy.data.tobytes())
        r.set('csr_matrix_indices', sparse_matrix_copy.indices.tobytes())
        r.set('csr_matrix_indptr', sparse_matrix_copy.indptr.tobytes())
        r.set('csr_matrix_shape', np.array(sparse_matrix_copy.shape, dtype=np.int32).tobytes())
        if not created:
            return Response({'error': 'Already following this user'}, status=400)

        return Response(True)

    def delete(self, request, *args, **kwargs):
        following_id = request.data.get('following_id')
        print(f"DELETE: Following id is: {following_id}")
        if not following_id:
            return Response({'error': 'following_id is required'}, status=400)

        try:
            following = CustomUser.objects.get(id=following_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        follow = Follow.objects.filter(follower=request.user, following=following).first()
        r = redis.Redis(host='localhost', port=6379, db=0)
   
        csr_matrix_data = np.frombuffer(r.get('csr_matrix_data'), dtype=np.int32)
        csr_matrix_indices = np.frombuffer(r.get('csr_matrix_indices'), dtype=np.int32)
        csr_matrix_indptr = np.frombuffer(r.get('csr_matrix_indptr'), dtype=np.int32)
        csr_matrix_shape = np.frombuffer(r.get('csr_matrix_shape'), dtype=np.int32)
        sparse_matrix = csr_matrix((csr_matrix_data, csr_matrix_indices, csr_matrix_indptr), shape=tuple(csr_matrix_shape))

        user_ids = list(CustomUser.objects.values_list("id", flat=True).order_by("id"))
        id_dict = dict(zip(user_ids, range(len(user_ids))))

        sparse_matrix_copy = sparse_matrix.copy() 

        sparse_matrix_copy[id_dict[request.user.id], id_dict[following_id]] = 1
        
        
        r.set('csr_matrix_data', sparse_matrix_copy.data.tobytes())
        r.set('csr_matrix_indices', sparse_matrix_copy.indices.tobytes())
        r.set('csr_matrix_indptr', sparse_matrix_copy.indptr.tobytes())
        r.set('csr_matrix_shape', np.array(sparse_matrix_copy.shape, dtype=np.int32).tobytes())
        if not follow:
            return Response({'error': 'Not following this user'}, status=400)

        follow.delete()

        print(self)

        return Response(True)