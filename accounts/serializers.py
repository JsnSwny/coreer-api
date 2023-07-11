from rest_framework import serializers
from .models import CustomUser, Follow, Language, Interest, Project, School, Education, WorkExperience, Question, UserAnswer, CareerLevel, ProjectImage
from django.contrib.auth import authenticate
from django.http import JsonResponse, response
import geocoder
from geopy.geocoders import Nominatim
from functools import partial
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.serializers import PasswordResetSerializer
from allauth.account.utils import (filter_users_by_email, user_pk_to_url_str, user_username)
from allauth.utils import build_absolute_uri
from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator
from allauth.account import app_settings
from dj_rest_auth.forms import AllAuthPasswordResetForm
from django.contrib.sites.shortcuts import get_current_site

class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):

    def clean_email(self):
        """
        Invalid email should not raise error, as this would leak users
        for unit test: test_password_reset_with_invalid_email
        """
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email, is_active=True)
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)
        current_site = get_current_site(request)
        
        for user in self.users:
            temp_key = token_generator.make_token(user)

            path = f"www.coreer.co/password_reset/{user_pk_to_url_str(user)}/{temp_key}/"
            # url = build_absolute_uri(request, path)
     #Values which are passed to password_reset_key_message.txt

            context = {
                "current_site": current_site,
                "user": user,
                "password_reset_url": path,
                "request": request,
                "path": path,
            }
            print(context)
            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )

        return self.cleaned_data['email']

class MyPasswordResetSerializer(PasswordResetSerializer):

    def validate_email(self, value):
        # use the custom reset form
        self.reset_form = CustomAllAuthPasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

# class ProjectImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectImage
#         fields = ('image',)



class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class CareerLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerLevel
        fields = '__all__'

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'

class UserAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    question_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Question.objects.all(), source="question")
    class Meta:
        model = UserAnswer
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all(),
        source='school',
        write_only=True
    )
    class Meta:
        model = Education
        fields = '__all__'

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ['provider', 'uid', 'extra_data']

class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'image',)

class ProjectSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(read_only=True, many=True)
    languages_id = serializers.CharField(write_only=True, required=False)
    images = serializers.SerializerMethodField()
    user = BasicUserSerializer(read_only=True, many=False)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', many=False, write_only=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'

    def get_images(self, obj):
        project_images = ProjectImage.objects.filter(project=obj)
        image_urls = [image.image.url for image in project_images]
        return image_urls
    
    def create(self, validated_data):
        languages_id = validated_data.pop('languages_id', None)
        if languages_id:
            language_ids = languages_id.split(',')  # Split comma-separated string into a list
            validated_data['languages'] = language_ids
        return super().create(validated_data)

    def update(self, instance, validated_data):
        languages_id = validated_data.pop('languages_id', None)
        if languages_id:
            language_ids = languages_id.split(',')  # Split comma-separated string into a list
            validated_data['languages'] = language_ids
        return super().update(instance, validated_data)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    # onboarded = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    languages = LanguageSerializer(read_only=True, many=True)
    interests = InterestSerializer(read_only=True, many=True)
    projects = ProjectSerializer(read_only=True, many=True)
    educations = EducationSerializer(read_only=True, many=True)
    work_experiences = WorkExperienceSerializer(read_only=True, many=True)
    interests_id = serializers.PrimaryKeyRelatedField(
        queryset=Interest.objects.all(), source='interests', many=True, write_only=True, required=False)
    languages_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), source='languages', many=True, write_only=True, required=False)
    projects_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), source='projects', many=True, write_only=True, required=False)
    work_experiences_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkExperience.objects.all(), source='work_experiences', many=True, write_only=True, required=False)
    
    user_answers = UserAnswerSerializer(read_only=True, many=True)

    current_level = CareerLevelSerializer(read_only=True)
    current_level_id = serializers.PrimaryKeyRelatedField(
        queryset=CareerLevel.objects.all(), source='current_level', write_only=True, required=False)
    
    looking_for = CareerLevelSerializer(read_only=True, many=True)
    looking_for_id = serializers.PrimaryKeyRelatedField(
        queryset=CareerLevel.objects.all(), source='looking_for', many=True, write_only=True, required=False)
    
    social_account = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'is_staff', 'username', 'image', 'social_account', 'user_answers', 'current_level', 'current_level_id', 'looking_for', 'looking_for_id', 'onboarded', 'work_experiences', 'work_experiences_id', 'educations', 'following', 'languages', 'languages_id', 'interests', 'interests_id', 'projects', 'projects_id', 'first_name', 'last_name', 'email', 'job', 'location', 'lat', 'lon', 'bio', 'profile_photo')
    
    def get_following(self, obj):
        follows = Follow.objects.filter(follower=obj).order_by('-followed_on')
        return list(follows.values_list("following", flat=True))
    
    def get_social_account(self, obj):
        social_account = SocialAccount.objects.filter(user=obj).first()
        if social_account:
            return SocialAccountSerializer(social_account).data
        return
    
class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = '__all__'

from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    # Exclude the username field
    username = None

    # Add your custom fields here
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    # Add any other fields you need for registration

    def custom_signup(self, request, user):
        # Set custom fields on the user object
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        # Set any other custom fields

        # Save the user object
        user.save()

# Register Serializer
class RegisterSerializer(RegisterSerializer):
    # onboarded = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    # def get_onboarded(self, obj):
    #     if obj.first_name and obj.first_name:
    #         return True
    #     return False

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        # g = geocoder.ip('me')
        # geolocator = Nominatim(user_agent="coreer")

        # location = geolocator.reverse(f"{g.lat},{g.lng}", language="en")
        user.lat = 55.953251
        user.lon = -3.188267

        user.location = f"City of Edinburgh, Scotland, United Kingdom"
        user.save()
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        data = dict(data)
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

# Profile Serializer
class ProfilesSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(read_only=True, many=True)
    projects = ProjectSerializer(read_only=True, many=True)
    educations = EducationSerializer(read_only=True, many=True)
    work_experiences = WorkExperienceSerializer(read_only=True, many=True)
    interests = InterestSerializer(read_only=True, many=True)
    user_answers = UserAnswerSerializer(read_only=True, many=True)
    looking_for = CareerLevelSerializer(read_only=True, many=True)
    current_level = CareerLevelSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'user_answers', 'interests', 'current_level', 'looking_for', 'work_experiences', 'image', 'first_name', 'last_name', 'onboarded', 'languages', 'educations', 'projects', 'email', 'job', 'location', 'lat', 'lon', 'bio', 'profile_photo')