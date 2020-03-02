import re
from rest_framework.permissions import BasePermission
from users.models import WebRes


class UserPermission(BasePermission):
    message = 'sorry, no permission'

    def has_permission(self, request, view):
        'all has'
        if request.user.is_superuser:
            return True
        return self.has_permission_detail(request)

    def has_object_permission(self, request, view, obj):
        return True

    def has_permission_detail(self, request):
        method = request.method.lower()
        path = re.sub(r'(/\d+/)', '/id/', request.path)
        try:
            web = WebRes.objects.filter(method=method, path=path).first()
            perms_list = request.user.role.resource.values_list('id', flat=True)
            if web and web.id in perms_list:
                return True
        except:
            import traceback
            traceback.print_exc()
        return False
