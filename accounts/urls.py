from django.urls import path, include
from .api import UserAPI, RetrieveProfile, UpdateUserViewSet, FollowAPIView, InterestViewSet, ProjectViewSet, SchoolViewSet, EducationViewSet, WorkExperienceViewSet, QuestionList, UserAnswerViewSet, CareerLevelList
from .views import GitHubLogin, exchange_code_for_access_token

from .views import get_popular_languages
from rest_framework import routers
router = routers.DefaultRouter()
router.register('user', UpdateUserViewSet, 'user')
router.register('interests', InterestViewSet, 'interests')
router.register('follow', FollowAPIView, 'follow')
router.register('projects', ProjectViewSet, 'projects')
router.register('schools', SchoolViewSet, 'schools')
router.register('educations', EducationViewSet, 'educations')
router.register('work-experiences', WorkExperienceViewSet, 'work-experiences')
router.register('user-answers', UserAnswerViewSet, 'work-experiences')

urlpatterns = [
    path('most-popular-languages/', get_popular_languages),
    path('api/auth/alt-user/', UserAPI.as_view()),
    path('accounts/', include('allauth.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('exchange-token/', exchange_code_for_access_token, name="exchange_token"),
    path('api/github/', GitHubLogin.as_view(), name='github_login'),
    path('api/questions/', QuestionList.as_view(), name="question-list"),
    path('api/career-levels/', CareerLevelList.as_view(), name="career-level-list"),
    path('api/profiles/<str:username>/', RetrieveProfile.as_view(), name="profiles-list"),
    path('api/', include(router.urls)),
]