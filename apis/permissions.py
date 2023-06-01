from rest_framework import permissions
from .models import User, Message


class IsGardenOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id.id == request.user.id


class IsGardenPhotoOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        garden = obj.garden_id
        if request.method in permissions.SAFE_METHODS:
            return True
        return garden.user_id.id == request.user.id


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
            return any(conversation.chat_sender_id == request.user or conversation.chat_receiver_id == request.user for conversation in queryset)

        return True


class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if isinstance(obj, Message):
            conversation = obj.conversation_id
        else:
            conversation = obj.conversation
        return (
            conversation.chat_sender_id == user or conversation.chat_receiver_id == user
        )
