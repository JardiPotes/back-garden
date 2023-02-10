from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import serializers
from .serializers import AuthUserSerializer
from .utils import create_user_account, get_and_authenticate_user

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        "login": serializers.UserLoginSerializer,
        "register": serializers.UserRegisterSerializer,
        "password_change": serializers.PasswordChangeSerializer,
    }

    @action(
        methods=[
            "POST",
        ],
        detail=False,
        permission_classes=[
            AllowAny,
        ],
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def login(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        login(request, user)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def logout(self, request):
        logout(request)
        data = {"success": "Sucessfully logged out"}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


# TODO Implement update user function
class UserViewSet(viewsets.ViewSet):
    permission_classes = [
        AllowAny,
    ]
    queryset = User.objects.all()

    def list(self, request):
        serializer = serializers.AuthUserSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        user = get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.AuthUserSerializer(user)
        return Response(serializer.data)
