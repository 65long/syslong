from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class WebRes(models.Model):
    'caidan'
    name = models.CharField(verbose_name='caidan', max_length=20, unique=True, null=True, blank=True)
    icon = models.CharField(verbose_name='tubiao', max_length=50, null=True, blank=True)
    path = models.CharField(verbose_name='url', max_length=200, null=True, blank=True)
    is_menu = models.BooleanField(verbose_name='shifoucaidan', default=False)
    sort = models.IntegerField(verbose_name='paixu', null=True, blank=True, default=100)
    pid = models.ForeignKey(verbose_name='fujicaidan', to='self', null=True, blank=True)
                
    def __str__(self):
        return self.name


class Role(models.Model):
    'juese'
    name = models.CharField(verbose_name='jueseming', max_length=20, unique=True)
    resource = models.ManyToManyField(verbose_name='webres', to='WebRes')
    desc = models.CharField(verbose_name='desc', max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    'yonghu'
    nickname = models.CharField(verbose_name='xingming', max_length=200, null=True, blank=True)
    mobile = models.CharField(verbose_name='shuji', max_length=11, null=True, blank=True)
    role = models.ForeignKey(verbose_name='yonghujuese', to='Role', related_name='role', null=True)
    
    def __str__(self):
        return self.username


