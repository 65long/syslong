# encoding: utf-8

from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Organization(models.Model):
    node_type_choice = ((1, '机构'), (2, '部门'))
    name = models.CharField(verbose_name='组织/部门名称', max_length=20)
    code_name = models.CharField(verbose_name='公司域名', max_length=20, unique=True, null=True)
    code_link = models.CharField(verbose_name='组织链接', max_length=200)
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
    is_menu = models.BooleanField(verbose_name='是否为菜单', default=False)
    level = models.PositiveSmallIntegerField(verbose_name='菜单级别', choices=level_choice)
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, default=100)
    pid = models.ForeignKey(verbose_name='父级权限', to='self', null=True, blank=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        temp = str('---父级节点---' + self.pid.name) if self.pid else '---根节点'
        return self.name + temp

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name


class Role(models.Model):
    '角色/职位'
    mode_choice = ((1, '系统所有'), (2, '本机构及下属机构'), (3, '本机构'),
                   (4, '本部门及下属部门'), (5, '本部门'), (6, '仅本人'))
    name = models.CharField(verbose_name='角色名称', max_length=20, unique=True)
    resource = models.ManyToManyField(verbose_name='角色的用户', to='WebResource', through='RoleResourceAssign',
                                     through_fields=('role', 'webres'))
    mode = models.PositiveSmallIntegerField(verbose_name='数据授权模式', choices=mode_choice)
    desc = models.CharField(verbose_name='描述', max_length=20, null=True, blank=True)
    dept = models.ForeignKey(verbose_name='所属部门', to='Organization', related_name='role_dept', null=True)
    org = models.ForeignKey(verbose_name='所属组织', to='Organization', related_name='role_org', null=True)
    is_active = models.BooleanField(verbose_name='是否有效', default=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
        unique_together = ('name', 'org',)


class RoleResourceAssign(models.Model):
    "role and moudle多对多第三张表自定义的"
    # mode_choice = (('系统所有', 1), ('本机构及下属机构', 2), ('本机构', 3),
    #                ('本部门及下属部门', 4), ('本部门', 5), ('仅本人', 6))
    method_choice = (('get', '获取'), ('post', '新增'), ('put', '更新'), ('delete', '删除'))
    role = models.ForeignKey(verbose_name='角色id', to='Role', related_name='web_role')
    webres = models.ForeignKey(verbose_name='模块id', to='WebResource', related_name='role_web')
    permission = models.BooleanField(verbose_name='允许访问', default=True)
    # 放在此处是针对某个模块是仅允许本人还是本部门，如果放在角色处是针对某个角色进行授权
    # mode = models.PositiveSmallIntegerField(verbose_name='数据授权模式', choices=mode_choice)
    method = models.CharField(verbose_name='操作行为/执行方法(针对api)', choices=method_choice, max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "角色权限表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '角色%s --权限%s'%(self.role, self.webres)


class UserProfile(AbstractUser):
    '扩展用户表'
    nickname = models.CharField(verbose_name='昵称', max_length=200, null=True, blank=True)
    mobile = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True)
    role = models.ForeignKey(verbose_name='用户角色', to='Role', related_name='user_role', null=True)
    dept = models.ForeignKey(verbose_name='用户部门', to='Organization', related_name='user_dept', null=True)
    org = models.ForeignKey(verbose_name='用户组织', to='Organization', related_name='user_org', null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name