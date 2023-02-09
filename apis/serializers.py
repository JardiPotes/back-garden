from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Garden, Photo


class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = ("id", "user_id", "title", "description", "address", "zipcode")


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("garden_id", "slug", "image", "isMainPhoto", "season")
