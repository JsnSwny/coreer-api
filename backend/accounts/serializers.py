from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    onboarded = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ('id', 'onboarded', 'first_name', 'last_name', 'email', 'likes')

    def get_onboarded(self, obj):
        if obj.first_name and obj.first_name:
            return True
        return False

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    onboarded = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ('id', 'onboarded', 'first_name', 'last_name', 'email', 'likes', 'password')
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
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'likes',)