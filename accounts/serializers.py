from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Garden, Photo

""" Deals with user creation

    Returns:
        user object with all fields
    """


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = (
            "id",
            "username",
            "password",
            "nickname",
            "email",
            "first_name",
            "last_name",
            "profile_image",
            "bio",
            "has_garden",
        )
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(**validated_data)
        return user


class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = ("id", "userId", "title", "description", "address", "zipcode")


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ("gardenId", "slug", "image", "isMainPhoto", "season")
