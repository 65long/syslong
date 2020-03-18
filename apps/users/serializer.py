# encoding: utf-8

import logging
from rest_framework import serializers
from .models import UserProfile, Role


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=100, source="role.name", read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'password', 'nickname', 'mobile', 'email', 'is_superuser', 'role']
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True},
                        'is_superuser': {'read_only': True},
                        }

    def create(self, validated_data):
        obj = super(UserSerializer, self).create(validated_data=validated_data)
        obj.set_password(validated_data.get('password'))
        obj.save()
        return obj

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
            validated_data.pop('password')
        print(validated_data)
        obj = super(UserSerializer, self).update(instance=instance, validated_data=validated_data)
        return obj


class RoleSerializer(serializers.ModelSerializer):
    perms = serializers.SerializerMethodField()
    cur_mode = serializers.CharField(source='get_mode_display', read_only=True)
    org = serializers.CharField(read_only=True)
    dept = serializers.CharField(read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'desc', 'cur_mode', 'org', 'dept', 'perms']
        extra_kwargs = {
            # 'password': {'write_only': True},
            # 'id': {'read_only': True},
            'cur_mode': {'read_only': True},
            }
        depth = 1

    def get_perms(self, role_obj):
        temp_dic = {}
        web_lst = role_obj.resource.all()
        # logging.info('web_list------{}'.format(web_lst))
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