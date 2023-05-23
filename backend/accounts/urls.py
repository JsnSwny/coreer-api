from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI, ProfilesViewSet, UpdateUserViewSet, FollowAPIView, InterestViewSet
from knox import views as knox_views


from .views import get_popular_languages
from rest_framework import routers
router = routers.DefaultRouter()
router.register('profiles', ProfilesViewSet, 'profiles')
router.register('user', UpdateUserViewSet, 'user')
router.register('interests', InterestViewSet, 'interests')
router.register('follow', FollowAPIView, 'follow')

urlpatterns = [
    path('api/auth/', include('knox.urls')),
    path('most-popular-languages/', get_popular_languages),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/', include(router.urls)),
    # path('api/follow/', FollowAPIView.as_view(), name='follow'),
]