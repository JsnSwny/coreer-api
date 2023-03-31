from rest_framework import serializers
from .models import CustomUser, Follow, Language, Interest, Project, School, Education
from django.contrib.auth import authenticate
from django.http import JsonResponse, response

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
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

class EducationSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    class Meta:
        model = Education
        fields = '__all__'

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    onboarded = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    languages = LanguageSerializer(read_only=True, many=True)
    interests = InterestSerializer(read_only=True, many=True)
    projects = ProjectSerializer(read_only=True, many=True)
    interests_id = serializers.PrimaryKeyRelatedField(
        queryset=Interest.objects.all(), source='interests', many=True, write_only=True, required=False)
    languages_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), source='languages', many=True, write_only=True, required=False)
    projects_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), source='projects', many=True, write_only=True, required=False)
    class Meta:
        model = CustomUser
        fields = ('id', 'onboarded', 'following', 'languages', 'languages_id', 'interests', 'interests_id', 'projects', 'projects_id', 'first_name', 'last_name', 'email', 'job', 'location', 'lat', 'lon', 'bio', 'profile_photo')

    def get_onboarded(self, obj):
        if obj.first_name and obj.last_name and len(obj.languages.all()) != 0 and len(obj.interests.all()) != 0:
            return True
        return False
    
    def get_following(self, obj):
        follows = Follow.objects.filter(follower=obj)
        return list(follows.values_list("following", flat=True))

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    onboarded = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ('id', 'onboarded', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def get_onboarded(self, obj):
        if obj.first_name and obj.first_name:
            return True
        return False

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
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
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'languages', 'educations', 'projects', 'email', 'job', 'location', 'lat', 'lon', 'bio', 'profile_photo')