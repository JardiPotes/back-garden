from django.contrib.auth import (authenticate, get_user_model,
                                 password_validation)
from django.contrib.auth.models import BaseUserManager
from django.core.validators import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apis.serializers import GardenSerializer

User = get_user_model()


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "bio",
            "has_garden",
            "profile_image",
            "gardens",
            "experience",
        )

    gardens = GardenSerializer(many=True, required=False)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(
        required=True, write_only=True, trim_whitespace=False
    )

    class meta:
        model = User
        fields = ("auth_token", "id")

    auth_token = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_auth_token(self, obj):
        token = Token.objects.get_or_create(user=obj)
        return token[0].key

    def get_id(self, obj):
        id = User.objects.get(email=obj.email).id
        return id


class EmptySerializer(serializers.Serializer):
    pass


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "nickname",
            "has_garden",
            "bio",
            "profile_image",
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "nickname",
            "has_garden",
            "bio",
            "profile_image",
            "experience",
        )

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class UserUpdateSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)
    has_garden = serializers.BooleanField(required=False)
    bio = serializers.CharField(
        style={"base_template": "textarea.html"}, required=False
    )
    profile_image = serializers.CharField(required=False)
    experience = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ("nickname", "has_garden", "bio", "profile_image", "experience")


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Current password does not match")
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
