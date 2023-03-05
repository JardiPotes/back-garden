from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError(
            "Invalid email/password. Please try again!")
    return user


def create_user_account(email, password, **extra_fields):
    user = get_user_model().objects.create_user(
        email=email, password=password, **extra_fields
    )
    return user


def temporary_image():
    import tempfile

    from PIL import Image

    image = Image.new("RGB", (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file, "jpeg")
    tmp_file.seek(0)
    return tmp_file
