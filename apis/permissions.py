from rest_framework import permissions


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
        if request.method != "POST":
            queryset = view.get_queryset()
            return any(
                conversation.chat_sender_id == request.user
                or conversation.chat_receiver_id == request.user
                for conversation in queryset
            )
        return True


class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        conversation = obj.conversation
        return (
            conversation.chat_sender_id == user or conversation.chat_receiver_id == user
        )
