from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import ProfilesSerializer, UserSerializer, LoginSerializer, RegisterSerializer, FollowSerializer, InterestSerializer, ProjectSerializer, SchoolSerializer, EducationSerializer, WorkExperienceSerializer, QuestionSerializer, UserAnswerSerializer, CareerLevelSerializer, ProjectImageSerializer, LanguageSerializer
from .models import CustomUser, Follow, Interest, Project, School, Education, WorkExperience, Question, UserAnswer, CareerLevel, ProjectImage, Language
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
from rest_framework.decorators import action

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

class UsersList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = CustomUser.objects.all()
    serializer_class = ProfilesSerializer
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

class RetrieveProfile(generics.RetrieveAPIView):
    serializer_class = ProfilesSerializer

    def get_object(self):
        username = self.kwargs['username']
        obj = get_object_or_404(CustomUser.objects.filter(username=username))
        return obj
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_visible']

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')
    

    @action(detail=True, methods=['post'])
    def pin(self, request, pk=None):
        project = self.get_object()
        user = request.user

        # Unpin the currently pinned project (if any)
        user.projects.filter(is_pinned=True).update(is_pinned=False)

        # Pin the selected project
        project.is_pinned = True
        project.save()

        return Response({'message': 'Project pinned successfully.'})
    
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
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
        return Follow.objects.filter(follower=self.user)
    

    
class UserAnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer


class QuestionList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

class InterestList(generics.ListAPIView):
    # permission_classes = [
    #     permissions.IsAuthenticated,
    # ]
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

    def get_queryset(self):
        return Interest.objects.all()
    
class LanguageList(generics.ListAPIView):
    # permission_classes = [
    #     permissions.IsAuthenticated,
    # ]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    def get_queryset(self):
        return Language.objects.all()

class CareerLevelList(generics.ListAPIView):
    # permission_classes = [
    #     permissions.IsAuthenticated,
    # ]
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
    serializer_class = EducationSerializer

    def get_queryset(self):
        return Education.objects.filter(user=self.user)
    
class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer

    def get_queryset(self):
        return WorkExperience.objects.filter(user=self.user)
    

class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project__id']

    def get_queryset(self):
        return ProjectImage.objects.all()
    

class FollowAPIView(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['follower__id']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['followed_on']

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def create(self, request, *args, **kwargs):
        following_id = request.data.get('following_id')
        if not following_id:
            return Response({'error': 'following_id is required'}, status=400)
        

        try:
            following = CustomUser.objects.get(id=following_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following)

        return Response(True)

    def delete(self, request, *args, **kwargs):
        following_id = request.data.get('following_id')
        if not following_id:
            return Response({'error': 'following_id is required'}, status=400)

        try:
            following = CustomUser.objects.get(id=following_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        follow = Follow.objects.filter(follower=request.user, following=following).first()

        follow.delete()

        return Response(True)