from rest_framework import serializers
from .models import CustomUser, Follow, Language, Interest, Project, School, Education, WorkExperience, Question, UserAnswer, CareerLevel
from django.contrib.auth import authenticate
from django.http import JsonResponse, response
import geocoder
from geopy.geocoders import Nominatim
from functools import partial
from allauth.socialaccount.models import SocialAccount

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'



class ProjectSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(read_only=True, many=True)
    class Meta:
        model = Project
        fields = '__all__'

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
        fields = ('id', 'image', 'social_account', 'user_answers', 'current_level', 'current_level_id', 'looking_for', 'looking_for_id', 'onboarded', 'work_experiences', 'work_experiences_id', 'educations', 'following', 'languages', 'languages_id', 'interests', 'interests_id', 'projects', 'projects_id', 'first_name', 'last_name', 'email', 'job', 'location', 'lat', 'lon', 'bio', 'profile_photo')
    
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
    class Meta:
        model = CustomUser
        fields = ('id', 'user_answers', 'interests', 'current_level', 'looking_for', 'work_experiences', 'image', 'first_name', 'last_name', 'onboarded', 'languages', 'educations', 'projects', 'email', 'job', 'location', 'lat', 'lon', 'bio', 'profile_photo')