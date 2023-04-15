from rest_framework import serializers

from accounts.models import User

from .models import Comment, Garden, Photo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "experience", "profile_image", "nickname")


class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = ("id", "user_id", "title", "description", "zipcode")


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "garden_id", "image", "is_main_photo", "season")


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, source="author_id")

    class Meta:
        model = Comment
        fields = (
            "id",
            "author_id",
            "author",
            "receiver_id",
            "content",
            "created_at",
            "updated_at",
        )
