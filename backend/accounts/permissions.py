from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    This permission is intended to only the authenticated user (request.user)
    has the power to change your own profile (obj.user)
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
