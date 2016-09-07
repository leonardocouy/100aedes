from rest_framework.permissions import BasePermission


class IsReportOwner(BasePermission):
    """
    This permission is intended to only the authenticated user (request.user)
    has the power to change your own report (obj.user)
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
