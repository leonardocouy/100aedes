from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReadOnlyOrAgent(BasePermission):
    """
    This permission is intended to only User's report (request.user)
    has the power to read your own report (obj.user)
    If (request.user) is a super-user or agent, he can use other operations
    """

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return request.method in SAFE_METHODS
        elif request.user.is_superuser:
            return True
        else:
            try:
                if request.user.groups.get(id=1).name == 'Agente':
                    return True
            except Group.DoesNotExist:
                return False
