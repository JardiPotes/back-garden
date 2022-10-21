from django.core import exceptions
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        errors = dict()
        try:
            validators.validate_password(password=password, user=user)

        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        hashed_password = make_password(password)
        data['password'] = hashed_password
        return super(UserSerializer, self).validate(data)
