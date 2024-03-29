from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apis.serializers import CommentSerializer, GardenSerializer

User = get_user_model()


class AuthUserSerializer(serializers.ModelSerializer):

    gardens = GardenSerializer(many=True, required=False)
    comments = CommentSerializer(
        many=True, required=False, source="receiver_comments")

    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "bio",
            "gardens",
            "profile_image",
            "experience",
            "comments",
        )

    def get_profile_image(self, user):
        request = self.context.get("request")
        if user.profile_image.url:
            request.build_absolute_uri(user.profile_image.url)
        else:
            default_profile_image_url = "accounts/images/default_profile_image.png"
            return request.build_absolute_uri(default_profile_image_url)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        max_length=300, required=True, write_only=True)
    password = serializers.CharField(
        required=True, write_only=True, trim_whitespace=False
    )

    auth_token = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_auth_token(self, obj):
        token = Token.objects.get_or_create(user=obj)
        return token[0].key

    def get_id(self, obj):
        id = User.objects.get(email=obj.email).id
        return id

    class Meta:
        model = User
        fields = ("id", "email", "password", "auth_token")
        extra_kwargs = {"email": {"write_only": True},
                        "password": {"write_only": True}}


class EmptySerializer(serializers.Serializer):
    pass


class UserRegisterSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)
    bio = serializers.CharField(
        style={"base_template": "textarea.html"}, required=False
    )
    profile_image = serializers.ImageField(required=False)
    experience = serializers.IntegerField(
        required=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "nickname",
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
    bio = serializers.CharField(
        style={"base_template": "textarea.html"}, required=False
    )
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ("nickname", "bio", "profile_image", "experience")


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError(
                "Current password does not match")
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
