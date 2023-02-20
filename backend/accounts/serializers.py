from rest_framework import serializers
from .models import CustomUser, Follow, Language
from django.contrib.auth import authenticate
from django.http import JsonResponse, response

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    onboarded = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    languages = LanguageSerializer(read_only=True, many=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'onboarded', 'following', 'languages', 'first_name', 'last_name', 'email', 'job', 'location', 'lat', 'lon', 'bio', 'profile_photo')

    def get_onboarded(self, obj):
        if obj.first_name and obj.first_name:
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
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'languages', 'email', 'job', 'location', 'lat', 'lon', 'bio', 'profile_photo')