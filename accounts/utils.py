from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.core.exceptions import ValidationError


def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid email/password. Please try again!")
    return user


def create_user_account(email, password, **extra_fields):
    user = get_user_model().objects.create_user(email=email, password=password, **extra_fields)
    return user


def validate_min_max_value_for_exp(value):
    if value in range(1, 6):
        return value
    else:
        raise ValidationError("The range of experiences should be at a scale of 1 to 5")
