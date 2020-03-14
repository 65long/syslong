# encoding: utf-8

from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class WebRes(models.Model):
    '菜单表'
    name = models.CharField(verbose_name='权限名称', max_length=20, unique=True, null=True, blank=True)
    icon = models.CharField(verbose_name='图标', max_length=50, null=True, blank=True)
    path = models.CharField(verbose_name='访问url', max_length=200, null=True, blank=True)
    is_menu = models.BooleanField(verbose_name='是否为菜单', default=False)
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, default=100)
    method = models.CharField(verbose_name='请求方法', max_length=20, null=True, blank=True)
    pid = models.ForeignKey(verbose_name='父级权限', to='self', null=True, blank=True)

    def __str__(self):
        temp = str('---父级节点---' + self.pid.name) if self.pid else '---根节点'
        return self.name + temp

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name


class Department(models.Model):
    name = models.CharField(verbose_name='部门名称', max_length=20)
    org = models.ForeignKey(verbose_name='所属组织', to='Organization', related_name='organization', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "部门表"
        verbose_name_plural = verbose_name
        unique_together = ('name', 'org',)


class UserProfile(AbstractUser):
    '扩展用户表'
    nickname = models.CharField(verbose_name='昵称', max_length=200, null=True, blank=True)
    mobile = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True)
    role = models.ForeignKey(verbose_name='用户角色', to='Role', related_name='role', null=True)
    department = models.ForeignKey(verbose_name='用户部门', to='Department', related_name='department', null=True)
    org = models.ForeignKey(verbose_name='用户组织', to='Organization', related_name='org', null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name


class Organization(models.Model):
    node_type_choice = (('机构', 1), ('部门', 2), ('职位', 3))
    name = models.CharField(verbose_name='名称', max_length=20)
    # domain = models.CharField(verbose_name='公司域名', max_length=20, unique=True, null=True)
    parent_node = models.ForeignKey(verbose_name='所属组织', to='self', related_name='parent', null=True)
    node_type = models.PositiveSmallIntegerField(verbose_name='节点类型', choices=node_type_choice)
    alias = models.CharField(verbose_name='别名', max_length=20)
    fullname = models.CharField(verbose_name='全称', max_length=20)
    is_active = models.BooleanField(verbose_name='是否有效', default=True)
    create_user = models.ForeignKey(verbose_name='创建者', to='UserProfile')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "组织机构"
        verbose_name_plural = verbose_name


class WebResource(models.Model):
    "系统功能模块"
    level_choice = (('模块', 1), ('子模块', 2), ('接口', 3))
    name = models.CharField(verbose_name='模块名称', max_length=20)
    parent_moudle = models.ForeignKey(verbose_name='父级模块', to='self', related_name='parent')
    moudle_level = models.PositiveSmallIntegerField(verbose_name='模块级别', choices=level_choice)
    # data_table = models.CharField(verbose_name='模块主数据表名称', max_length=20, null=True, blank=True)
    desc = models.CharField(verbose_name='模块描述', max_length=20)
    create_user = models.OneToOneField(verbose_name='创建者', to='UserProfile')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)


class Role(models.Model):
    '角色/职位'
    mode_choice = (('系统所有', 1), ('本机构及下属机构', 2), ('本机构', 3),
                   ('本部门及下属部门', 4), ('本部门', 5), ('仅本人', 6))
    name = models.CharField(verbose_name='角色名称', max_length=20, unique=True)
    users = models.ManyToManyField(verbose_name='角色的用户', to='UserProfile')
    moudles = models.ManyToManyField(verbose_name='角色的用户', to='WebResource', through='RolerResourceAssign',
                                     through_fields=('role', 'moudle'))
    mode = models.PositiveSmallIntegerField(verbose_name='数据授权模式', choices=mode_choice)
    desc = models.CharField(verbose_name='描述', max_length=20, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='是否有效', default=True)
    create_user = models.OneToOneField(verbose_name='创建者', to='UserProfile')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name


class RolerResourceAssign(models.Model):
    "role and moudle多对多第三张表自定义的"
    # mode_choice = (('系统所有', 1), ('本机构及下属机构', 2), ('本机构', 3),
    #                ('本部门及下属部门', 4), ('本部门', 5), ('仅本人', 6))
    method_choice = (('获取', 'get'), ('新增', 'post'), ('更新', 'put'), ('删除', 'delete'),)
    role = models.ForeignKey(verbose_name='角色id', to='Role', related_name='role')
    moudle = models.ForeignKey(verbose_name='模块id', to='WebResource', related_name='moudle')
    permission = models.BooleanField(verbose_name='允许访问', default=True)
    # 放在此处是针对某个模块是仅允许本人还是本部门，如果放在角色处是针对某个角色进行授权
    # mode = models.PositiveSmallIntegerField(verbose_name='数据授权模式', choices=mode_choice)
    method = models.CharField(verbose_name='操作行为/执行方法(针对api)', choices=method_choice)

