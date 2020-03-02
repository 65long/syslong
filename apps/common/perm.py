from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    message = 'sorry, no permission'

    def has_permission(self, request, view):
        'all has'
        print(request.path)
        if request.user.is_superuser:
            return True
        return self.has_permission_detail(request)

    def has_object_permission(self, request, view, obj):
        return True

    def has_permission_detail(self, request):
        return False
