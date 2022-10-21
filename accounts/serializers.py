from django.core import exceptions
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
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


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'email': {'write_only': True},
                        'password': {'write_only': True}}

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = 'Access denied: wrong email or password.'
                raise AuthenticationFailed(
                    msg, code='authentication_failed')

        else:
            msg = 'Both "email" and "password" are required.'
            raise AuthenticationFailed(
                msg, code='authentication_failed')
        attrs['user'] = user
        return attrs
