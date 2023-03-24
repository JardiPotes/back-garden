from rest_framework import serializers

from .models import Comment, Garden, Photo


class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = ("id", "user_id", "title", "description", "zipcode")


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("garden_id", "slug", "image", "isMainPhoto", "season")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "author_id",
            "receiver_id",
            "content",
            "created_at",
            "updated_at",
        )
