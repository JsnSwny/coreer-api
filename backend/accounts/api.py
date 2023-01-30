from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import ProfilesSerializer, UserSerializer, LoginSerializer, RegisterSerializer
from .models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.contrib.auth import login

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        print("API")
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
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
        return Response(serializer.data)

# Get User API

class ProfilesViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfilesSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_object(self):
        obj = get_object_or_404(CustomUser.objects.filter(id=self.kwargs["pk"]))
        return obj

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)