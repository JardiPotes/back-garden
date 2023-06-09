from rest_framework import permissions

from django.shortcuts import get_object_or_404
from .models import User, Message, Garden


class IsGardenOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsGardenPhotoOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        garden = get_object_or_404(Garden, pk=obj.garden_id)
        if request.method in permissions.SAFE_METHODS:
            return True
        return garden.user == request.user


class IsCommentOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author_id == request.user


class IsConversationMembersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        current_user_id = request.query_params.get('current_user_id', None)

        if current_user_id:
            try:
                User.objects.get(id=current_user_id)
            except User.DoesNotExist:
                return False

        if request.method != "POST":
            queryset = view.get_queryset()
            return any(conversation.chat_sender_id == request.user.id or conversation.chat_receiver_id == request.user.id for conversation in queryset)

        return True


class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        if isinstance(obj, Message):
            conversation = obj.conversation
        else:
            conversation = obj
        return (
            conversation.chat_sender_id == user_id or conversation.chat_receiver_id == user_id
        )
