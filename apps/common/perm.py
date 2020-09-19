import re
from rest_framework.permissions import BasePermission
from users.models import WebResource


class UserPermission(BasePermission):
    message = 'sorry, no permission'

    def has_permission(self, request, view):
        'all has'
        if not request.user.is_authenticated():
            # 未登录认证
            return False
        if request.user.is_superuser and request.user.is_active:
            return True
        return self.has_permission_detail(request)

    def has_object_permission(self, request, view, obj):
        return True

    def has_permission_detail(self, request):
        method = request.method.lower()
        path = re.sub(r'(/\d+/)', '/id/', request.path)
        try:
            web = WebResource.objects.filter(method=method, path=path).first()
            perms_list = request.user.role.resource.values_list('id', flat=True)
            if web and web.id in perms_list:
                return True
        except:
            import traceback
            traceback.print_exc()
        return False

    def get_data_perms(self, role):
        """    mode_choice = ((1, '系统所有'), (2, '本机构及下属'), (3, '仅本机构'),
                   (4, '本部门及下属'), (5, '仅本部门'), (6, '仅本人'))"""
        from django.db.models import Q
        from users.models import Organization
        res_lst = []
        org_dept = []
        user_id = []
        if role.mode == 1:
            #  系统所有不进行数据权限过滤"Q(id=perm_id) | Q(pid=perm_id)"
            pass
        elif role.mode == 2:
            # 本机构及其下属
            Organization.object.filter(Q(id=role.org_id) | Q(parent_node=role.org_id)).values_list('id', flat=True)
        elif role.mode == 3:
            pass
        elif role.mode == 4:
            pass
        elif role.mode == 5:
            pass
        elif role.mode == 6:
            pass

