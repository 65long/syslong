# encoding: utf-8

import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Organization(models.Model):
    node_type_choice = ((1, '机构'), (2, '部门'))
    name = models.CharField(verbose_name='组织/部门名称', max_length=20)
    code_name = models.CharField(verbose_name='公司域名', max_length=20, unique=True, null=True, blank=True)
    code_link = models.CharField(verbose_name='快查链接', max_length=2000, default=uuid.uuid4())
    parent_node = models.ForeignKey(verbose_name='父节点', to='self', related_name='parent', null=True, blank=True)
    node_type = models.PositiveSmallIntegerField(verbose_name='节点类型', choices=node_type_choice)
    alias = models.CharField(verbose_name='别名', max_length=20, null=True, blank=True)
    fullname = models.CharField(verbose_name='全称', max_length=20, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='是否有效', default=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "组织部门"
        verbose_name_plural = verbose_name


class WebResource(models.Model):
    '菜单表'
    level_choice = ((1, '模块'), (2, '子模块'), (3, 'api接口'))
    name = models.CharField(verbose_name='权限名称', max_length=20, unique=True, null=True, blank=True)
    path = models.CharField(verbose_name='访问url', max_length=200, null=True, blank=True)
    component = models.CharField(verbose_name='前端组件', max_length=300, default=r'login/Login')
    component_name = models.CharField(verbose_name='前端组件名称', max_length=100, default=r'Login')
    icon = models.CharField(verbose_name='前端图标', max_length=100, default='tree-table')
    is_menu = models.BooleanField(verbose_name='是否为菜单', default=False)
    code_link = models.CharField(verbose_name='快查链接', max_length=2000, null=True, blank=True)
    level = models.PositiveSmallIntegerField(verbose_name='菜单级别', choices=level_choice)
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, default=100)
    # 删除父级菜单，子菜单的pid设置为None(子菜单变为根菜单)
    pid = models.ForeignKey(verbose_name='父级权限', to='self', null=True, blank=True, on_delete=models.SET_NULL)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        temp = str('---父级节点---' + self.pid.name) if self.pid else '---根节点'
        return self.name + temp

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name


# class RoleGroup(models.Model):
#     """角色组"""
#     name = models.CharField(verbose_name='角色组名称', max_length=50, unique=True)


class Role(models.Model):
    '角色/职位'
    mode_choice = ((1, '系统所有'), (2, '本机构及下属'), (3, '仅本机构'),
                   (4, '本部门及下属'), (5, '仅本部门'), (6, '仅本人'))
    # 总管理员有全部权限， 权限授权分管理员/分管理员可以管理本部门或者多个部门， 主管管理本部门， 普通角色为
    type_choice = ((1, '总管理员'), (2, '分管理员'), (3, '主管'),
                   (4, '普通角色'))
    name = models.CharField(verbose_name='角色名称', max_length=20, unique=True)
    resource = models.ManyToManyField(verbose_name='角色的菜单', to='WebResource', through='RoleResourceAssign',
                                     through_fields=('role', 'webres'))
    # dept = models.ForeignKey(verbose_name='所属部门', to='Organization', related_name='role_dept', null=True)
    # org = models.ForeignKey(verbose_name='所属组织', to='Organization', related_name='role_org', null=True)
    mode = models.PositiveSmallIntegerField(verbose_name='授权范围', choices=mode_choice, default=6)
    role_type = models.PositiveSmallIntegerField(verbose_name='角色类型', choices=type_choice, default=4)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)
    desc = models.CharField(verbose_name='描述', max_length=20, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='是否有效', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
        # unique_together = ('name', 'org',)


class RoleResourceAssign(models.Model):
    "role and moudle多对多第三张表自定义的"
    method_choice = (('get', '获取'), ('post', '新增'), ('put', '更新'), ('delete', '删除'))
    role = models.ForeignKey(verbose_name='角色id', to='Role', related_name='web_role')
    webres = models.ForeignKey(verbose_name='模块id', to='WebResource', related_name='role_web')
    permission = models.BooleanField(verbose_name='允许访问', default=True)
    method = models.CharField(verbose_name='操作行为/执行方法(针对api)', choices=method_choice, max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "角色的权限"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '角色%s --权限%s'%(self.role, self.webres)


class UserProfile(AbstractUser):
    '扩展用户表'

    def gen_image_name(_instance, filename):
        import hashlib
        hash = hashlib.sha256(_instance.username[::-1].encode('utf-8'))
        filename = hash.hexdigest()[::-1] + '.' + filename.split('.')[-1]
        return 'user/head/img/{}'.format(filename)

    nickname = models.CharField(verbose_name='昵称', max_length=200, null=True, blank=True)
    mobile = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True)
    head_img = models.ImageField(verbose_name='用户头像', upload_to=gen_image_name, default='default.png')
    role = models.ManyToManyField(verbose_name='用户角色', to='Role', related_name='role_user')
    dept = models.ManyToManyField(verbose_name='用户组织', to='Organization', related_name='dept_user')
    position = models.CharField(verbose_name='职位', max_length=20, null=True, blank=True)
    show_tagsview = models.BooleanField(verbose_name='开启页签模式', blank=True, default=True)
    show_avatar = models.BooleanField(verbose_name='导航栏显示头像', blank=True, default=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "系统用户"
        verbose_name_plural = verbose_name