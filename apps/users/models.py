# encoding: utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class WebRes(models.Model):
    '菜单'
    name = models.CharField(verbose_name='权限名称', max_length=20, unique=True, null=True, blank=True)
    icon = models.CharField(verbose_name='图标', max_length=50, null=True, blank=True)
    path = models.CharField(verbose_name='访问url', max_length=200, null=True, blank=True)
    is_menu = models.BooleanField(verbose_name='是否为菜单', default=False)
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, default=100)
    method = models.CharField(verbose_name='请求方法', max_length=20, null=True, blank=True)
    pid = models.ForeignKey(verbose_name='父级权限', to='self', null=True, blank=True)
                
    def __str__(self):
        return self.name


class Role(models.Model):
    '角色'
    name = models.CharField(verbose_name='角色名称', max_length=20, unique=True)
    resource = models.ManyToManyField(verbose_name='权限', to='WebRes')
    desc = models.CharField(verbose_name='描述', max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    '扩展用户表'
    nickname = models.CharField(verbose_name='昵称', max_length=200, null=True, blank=True)
    mobile = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True)
    role = models.ForeignKey(verbose_name='用户角色', to='Role', related_name='role', null=True)
    
    def __str__(self):
        return self.username


