from rest_framework import permissions


class IsGardenOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id.id == request.user.id


class IsCommentOwnerPermission(permissions.BasePermission):
    def has_comment_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author_id.id == request.user.id
