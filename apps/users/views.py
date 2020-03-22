# encoding: utf-8
import datetime

from django.shortcuts import render
from django.core.cache import caches
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate as auth
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import WebResource, UserProfile, Role, RoleResourceAssign, Organization
from .serializer import UserSerializer, RoleSerializer
from .filter import UserFilter
import logging

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# Create your views here.

ROLE_MODE_DICT = dict(Role.mode_choice)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            role = user.role.name if hasattr(user.role, 'name') else '未分配角色'
            data = dict(token=token, username=user.username, role=role, status=200)
            seconds = settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA', datetime.timedelta(minutes=0)).total_seconds()
            caches["redis-token"].set(token, user, seconds)
            return Response(data, 200)
        data = dict(message='用户名或密码错误', status=401)
        return Response(data, 401)


class MenuView(APIView):
    """  // 返回值为[{示例如下}, {}]
  // path: '/research',
  // component: Layout,
  // redirect: '/research/respage01',
  // name: 'Research',
  // alwaysShow: true,
  // meta: { title: '刘福龙', icon: 'wechat' },
  // children: []  """
    permission_classes = []

    def get(self, request, *args, **kwargs):
        '获取系统的菜单列表用于前端展示'
        if request.user.is_superuser:
            # 系统最高权限管理猿菜单不受分配影响，直接查数据库
            webres = WebResource.objects.filter(is_menu=True).all()
        else:
            webres = request.user.role.resource.filter(is_menu=True).all()
        res = []
        temp_dic = {}
        try:
            for web in webres:
                    # logging.info('web pid----%s' %web.pid)
                    if web.pid is None:
                        rank1router = {'name': web.component_name, 'path': web.path, 'component': 'Layout',
                                       'redirect': "noredirect", 'alwaysShow': True,
                                       'meta': {'title': web.name, 'icon': web.icon}}
                        if web.id not in temp_dic:
                            rank1router.update({'children': []})
                            temp_dic[web.id] = rank1router
                        else:
                            temp_dic[web.id].update(rank1router)
                    else:
                        rank2router = {'name': web.component_name, 'path': web.path, 'component': web.component,
                                       'alwaysShow': False,
                                       'meta': {'title': web.name, 'icon': web.icon}}
                        if web.pid.id not in temp_dic:
                            temp_dic[web.pid.id] = {'children': [rank2router]}
                        else:
                            temp_dic[web.pid.id]['children'].append(rank2router)
        except Exception:
            logging.info('temp-dict----{}'.format(temp_dic))
            import traceback
            traceback.print_exc()
        return Response({'menu_list': temp_dic.values()})


class PermsListView(APIView):
    permission_classes = []

    # 获取当前用户有的权限
    def get(self, request,*args, **kwargs):
        res = []
        try:
            webres = request.user.role.resource.filter(is_menu=True).all()
            for web in webres:
                if web.pid is None:
                    res.append(dict(name=web.name, path=web.path, level='一级'))
                else:
                    res.append(dict(name=web.name, path=web.path, level='二级'))
        except Exception as e:
            logging.error('获取当前用户权限失败%s' %e)
        return Response(res)


class PermsView(APIView):
    '/api/rbac/perms'

    # 用户权限数据的增删改查,针对权限本身的增删改查不提供前台接口
    def get(self, request, *args, **kwargs):
        "当前用户有的权限"
        perms_id_lst = []
        # 所有权限
        res = self.get_perms_all()
        role_id = request.query_params .get('role_id', -1)
        role = Role.objects.filter(id=role_id).first()
        if role:
            perms_id_lst = self.get_perms_id(role)
        return Response({'allperms': res, 'ownperms': perms_id_lst})

    def post(self, request, *args, **kwargs):
        '新增某个用户的权限'
        res_lst = []
        role_id = request.data.get('role_id', -1)
        perm_id = request.data.get('perm_id', [])
        role = Role.objects.filter(id=role_id).first()
        perms = WebResource.objects.filter(id__in=perm_id).all()
        # 为角色重新赋权限
        if role and perms:
            role.resource.clear()
            for perm in perms:
                RoleResourceAssign.objects.create(role=role, webres=perm)

            res_lst = self.get_perms(role)
        # 删除角色的所有权限
        elif role and not perms:
            role.resource.clear()
        return Response(res_lst)

    def delete(self, request, *args, **kwargs):
        '该方法为某个角色删除掉某些权限'
        from django.db.models import Q
        perms_lst = []
        res_lst = []
        role_id = request.data.get('role_id', -1)
        perm_id = request.data.get('perm_id', -1)
        role = Role.objects.filter(id=role_id).first()
        perms = WebResource.objects.filter(Q(id=perm_id) | Q(pid=perm_id)).values_list('id', flat=True)
        perms = WebResource.objects.filter(Q(id__in=perms) | Q(pid__in=perms)).values_list('id', flat=True)
        if role and perms:
            RoleResourceAssign.objects.filter(role=role, webres__in=perms).delete()
            res_lst = self.get_perms(role)
        return Response(res_lst)

    def get_perms(self, role_obj):
        temp_dic = {}
        web_lst = role_obj.resource.all()
        for web in web_lst:
            if web.pid is None:  # 一级权限
                if web.id not in temp_dic:
                    temp_dic[web.id] = {'id': web.id, 'name': web.name, 'path': web.path, 'children': {}}
                else:
                    temp_dic[web.id]['id'] = web.id
                    temp_dic[web.id]['name'] = web.name
                    temp_dic[web.id]['path'] = web.path
            else:  # 二级三级权限
                if web.pid.pid is None:  # 二级权限
                    child = {'id': web.id, 'name': web.name, 'path': web.path, 'children': {}}
                    if web.pid.id not in temp_dic:  # 二级权限的父级权限未加入
                        temp_dic[web.pid.id] = {'children': {web.id: child}}
                    else:  # 二级权限的父级权限已经存在
                        temp_dic[web.pid.id]['children'][web.id] = child
                else:  # 三级权限
                    child = {'id': web.id, 'name': web.name, 'path': web.path, 'children': {}}
                    # 三级权限的父级1级权限不存在
                    if web.pid.pid.id not in temp_dic:
                        temp_dic[web.pid.pid.id] = {'children': {}}
                    # 三级权限的父级2级权限不存在
                    if web.pid.id not in temp_dic[web.pid.pid.id]['children']:
                        temp_dic[web.pid.pid.id]['children'][web.pid.id] = {'children': {}}
                    # 直接更新三级权限
                    temp_dic[web.pid.pid.id]['children'][web.pid.id]['children'][web.id] = child

        temp_lst = []
        for r1 in temp_dic.values():
            r1_children = []
            for r2 in r1.get('children', {}).values():
                r2_children = []
                for r3 in r2.get('children', {}).values():
                    r3['children'] = []
                    r2_children.append(r3)

                r2['children'] = r2_children
                r1_children.append(r2)

            r1['children'] = r1_children
            temp_lst.append(r1)
        return temp_lst

    def get_perms_id(self, role_obj):
        res_lst = []
        web_res = role_obj.resource.filter(is_menu=False).all()
        for web in web_res:
            res_lst.append(web.id)
        return res_lst

    def get_perms_all(self):
        temp_dic = {}
        web_lst = WebResource.objects.all()
        for web in web_lst:
            if web.pid is None:  # 一级权限
                if web.id not in temp_dic:
                    temp_dic[web.id] = {'id': web.id, 'name': web.name, 'path': web.path, 'children': {}}
                else:
                    temp_dic[web.id]['id'] = web.id
                    temp_dic[web.id]['name'] = web.name
                    temp_dic[web.id]['path'] = web.path
            else:  # 二级三级权限
                if web.pid.pid is None:  # 二级权限
                    child = {'id': web.id, 'name': web.name, 'path': web.path, 'children': {}}
                    if web.pid.id not in temp_dic:  # 二级权限的父级权限未加入
                        temp_dic[web.pid.id] = {'children': {web.id: child}}
                    else:  # 二级权限的父级权限已经存在
                        temp_dic[web.pid.id]['children'][web.id] = child
                else:  # 三级权限
                    child = {'id': web.id, 'name': web.name, 'path': web.path, 'children': {}}
                    # 三级权限的父级1级权限不存在
                    if web.pid.pid.id not in temp_dic:
                        temp_dic[web.pid.pid.id] = {'children': {}}
                    # 三级权限的父级2级权限不存在
                    if web.pid.id not in temp_dic[web.pid.pid.id]['children']:
                        temp_dic[web.pid.pid.id]['children'][web.pid.id] = {'children': {}}
                    # 直接更新三级权限
                    temp_dic[web.pid.pid.id]['children'][web.pid.id]['children'][web.id] = child

        temp_lst = []
        for r1 in temp_dic.values():
            r1_children = []
            for r2 in r1.get('children', {}).values():
                r2_children = []
                for r3 in r2.get('children', {}).values():
                    r3['children'] = []
                    r2_children.append(r3)

                r2['children'] = r2_children
                r1_children.append(r2)

            r1['children'] = r1_children
            temp_lst.append(r1)
        return temp_lst


class UsersView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = UserFilter
    ordering_fields = ('id', )
    ordering = ('-id', )


class RoleToUsersView(APIView):

    def get(self, request, *args, **kwargs):
        return self.get_roles_all()

    def post(self, request, *args, **kwargs):
        role_id = request.data.get('role_id', 0)
        user_id = request.data.get('user_id', 0)
        user = UserProfile.objects.filter(id=user_id).first()
        role = Role.objects.filter(id=role_id).first()
        if user and role:
            user.role = role
            user.save()
        return Response(dict(role=getattr(role, 'name', '获取失败')))

    def get_roles_all(self):
        res_lst = []
        role_lst = Role.objects.all()
        for role in role_lst:
            res_lst.append(dict(id=role.id, name=role.name, mode=role.mode))
        return Response(res_lst)


class RoleView(ModelViewSet):
    '角色的权限的增删改查'
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class DataPermsToRole(APIView):
    "更改角色数据权限"
    def get(self, request, *args, **kwargs):
        cur_mode = 0
        try:
            cur_role = request.query_params .get('role_id', -1)
            role = Role.objects.filter(id=cur_role).first()
            cur_mode = str(role.mode) if hasattr(role, 'mode') else '0'
        except Exception as e:
            logging.info('获取角色数据权限异常 -%s' %e)
        org_dept_lst = self.get_org_dept()
        return Response(dict(all_dataperms=ROLE_MODE_DICT, cur_mode=cur_mode, org_dept_lst=org_dept_lst))

    def post(self, request, *args, **kwargs):
        org, dept, res_mode = (None, None, None)
        role_id = request.data.get('role_id', -1)
        mode = int(request.data.get('mode', -1))
        role = Role.objects.filter(id=role_id).first()
        try:
            if role and mode in ROLE_MODE_DICT:
                role.mode = mode
                org_type_lst = request.data.get('org_dept', "")
                # logging.info('-1---org_type_lst----%s' %1)
                args_len = len(org_type_lst)
                if args_len == 2:
                    role.org_id, role.dept_id = org_type_lst
                elif args_len == 1:
                    # 仅属于某个组织 清空所在部门
                    role.org_id = org_type_lst[0]
                    role.dept_id = None
                role.save()
                org, dept = getattr(role.org, 'name', None), getattr(role.dept, 'name', None)
                res_mode = ROLE_MODE_DICT.get(mode)
        except:
            import traceback
            traceback.print_exc()
        return Response(dict(mode=res_mode, org=org, dept=dept))

    def get_org_dept(self):
        orgs = Organization.objects.all()
        res_dict = {}
        for org in orgs:
            cur_org = dict(id=org.id, name=self.name_filter(org.name))
            # org
            if org.node_type == 1:
                if org.id not in res_dict:
                    res_dict[org.id] = dict(**cur_org, children=[])
                else:
                    res_dict[org.id]['id'] = org.id
                    res_dict[org.id]['name'] = org.name
            # dept
            elif org.node_type == 2:
                if org.parent_node.id not in res_dict:
                    res_dict[org.parent_node.id] = dict(children=[cur_org])
                else:
                    res_dict[org.parent_node.id]['children'].append(cur_org)
            else:
                pass

        return res_dict.values()

    def name_filter(self, name=''):
        if len(name) > 12 and isinstance(name, str):
            name = name[:2] + '...' + name[-2:]
        return name