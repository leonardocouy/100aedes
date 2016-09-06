from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    This permission is intended to only the authenticated user (request.user)
    has the power to change your own profile (obj.user)
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
