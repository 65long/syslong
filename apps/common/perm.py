from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    message = 'sorry, no permission'

    def has_permission(self, request, view):
        'all has'
        return True
