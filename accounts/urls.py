from django.urls import path, include
from .api import UserAPI, RetrieveProfile, FollowAPIView, ProjectViewSet, SchoolViewSet, EducationViewSet, WorkExperienceViewSet, QuestionList, UserAnswerViewSet, CareerLevelList, ProjectImageViewSet, UsersList, InterestList, LanguageList
from .views import GitHubLogin, exchange_code_for_access_token

from .views import get_popular_languages
from rest_framework import routers
router = routers.DefaultRouter()
router.register('follow', FollowAPIView, 'follow')
router.register('projects', ProjectViewSet, 'projects')
router.register('schools', SchoolViewSet, 'schools')
router.register('educations', EducationViewSet, 'educations')
router.register('work-experiences', WorkExperienceViewSet, 'work-experiences')
router.register('user-answers', UserAnswerViewSet, 'user-answers')
router.register('project-images', ProjectImageViewSet, 'project-images')

urlpatterns = [
    path('api/auth/alt-user/', UserAPI.as_view()),
    path('accounts/', include('allauth.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('exchange-token/', exchange_code_for_access_token, name="exchange_token"),
    path('api/github/', GitHubLogin.as_view(), name='github_login'),
    path('api/questions/', QuestionList.as_view(), name="question-list"),
    path('api/career-levels/', CareerLevelList.as_view(), name="career-level-list"),
    path('api/profiles/<str:username>/', RetrieveProfile.as_view(), name="profiles-list"),
    path('api/profiles/', UsersList.as_view(), name="get-users"),
    path('api/interests/', InterestList.as_view(), name="get-interests"),
    path('api/languages/', LanguageList.as_view(), name="get-languages"),
    path('api/', include(router.urls)),
]