from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate as auth
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import WebRes, UserProfile, Role
from .serializer import UserSerializer, RoleSerializer
from .filter import UserFilter
import logging

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# Create your views here.


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            data = dict(token=jwt_encode_handler(payload), username=user.username, status=200)
            return Response(data, 200)
        data = dict(message='auth failed', status=401)
        return Response(data, 401)


class MenuView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        '获取系统的菜单列表用于前端展示'
        if request.user.is_superuser:
            # 系统最高权限管理猿菜单不受分配影响，直接查数据库
            webres = WebRes.objects.filter(is_menu=True).all()
        else:
            webres = request.user.role.resource.filter(is_menu=True).all()
        # logging.info('webres-------{}'.format(webres))
        res = []
        temp_dic = {}
        for web in webres:
                logging.info('web pid----%s' %web.pid)
                if web.pid is None:
                    if web.id not in temp_dic:
                        temp_dic[web.id] = {'name': web.name, 'path': web.path, 'children': []}
                    else:
                        temp_dic[web.id]['name'] = web.name
                        temp_dic[web.id]['path'] = web.path
                else:
                    child = {'name': web.name, 'path': web.path}
                    if web.pid.id not in temp_dic:
                        temp_dic[web.pid.id] = {'children': [child]}
                    else:
                        temp_dic[web.pid.id]['children'].append(child)

        return Response({'menu': temp_dic.values()})


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
        perms = WebRes.objects.filter(id__in=perm_id).all()
        # 为角色重新赋权限
        if role and perms:
            role.resource.clear()
            role.resource.add(*perms)
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
        perms = WebRes.objects.filter(Q(id=perm_id) | Q(pid=perm_id)).all()
        perms_lst.extend(perms)
        # 添加一级权限寻找三级权限
        temp_perms = WebRes.objects.filter(pid=perm_id).all()
        for temp_perm in temp_perms:
            web3 = WebRes.objects.filter(pid=temp_perm.id).all()
            perms_lst.extend(web3)
        if role and perms_lst:
            role.resource.remove(*perms_lst)
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
            # print('r1--------', r1)
            r1_children = []
            for r2 in r1.get('children', {}).values():
                # print('r2--------', r2)
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
        web_lst = WebRes.objects.all()
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
            # print('r1--------', r1)
            r1_children = []
            for r2 in r1.get('children', {}).values():
                # print('r2--------', r2)
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
            res_lst.append(dict(id=role.id, name=role.name))
        return Response(res_lst)


class RoleView(ModelViewSet):
    '角色的权限的增删改查'
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    # filter_class = UserFilter
    # ordering_fields = ('id',)
    # ordering = ('-id',)
