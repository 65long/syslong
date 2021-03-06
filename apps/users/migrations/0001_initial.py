# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-03-17 13:22
from __future__ import unicode_literals

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(blank=True, max_length=200, null=True, verbose_name='昵称')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号')),
            ],
            options={
                'verbose_name': '用户信息表',
                'verbose_name_plural': '用户信息表',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='组织/部门名称')),
                ('code_name', models.CharField(max_length=20, null=True, unique=True, verbose_name='公司域名')),
                ('code_link', models.CharField(max_length=200, verbose_name='组织链接')),
                ('node_type', models.PositiveSmallIntegerField(choices=[(1, '机构'), (2, '部门')], verbose_name='节点类型')),
                ('alias', models.CharField(blank=True, max_length=20, null=True, verbose_name='别名')),
                ('fullname', models.CharField(blank=True, max_length=20, null=True, verbose_name='全称')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否有效')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('parent_node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='users.Organization', verbose_name='父节点')),
            ],
            options={
                'verbose_name': '组织部门',
                'verbose_name_plural': '组织部门',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='角色名称')),
                ('mode', models.PositiveSmallIntegerField(choices=[(1, '系统所有'), (2, '本机构及下属机构'), (3, '本机构'), (4, '本部门及下属部门'), (5, '本部门'), (6, '仅本人')], verbose_name='数据授权模式')),
                ('desc', models.CharField(blank=True, max_length=20, null=True, verbose_name='描述')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否有效')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('dept', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role_dept', to='users.Organization', verbose_name='所属部门')),
                ('org', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role_org', to='users.Organization', verbose_name='所属组织')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
            },
        ),
        migrations.CreateModel(
            name='RoleResourceAssign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.BooleanField(default=True, verbose_name='允许访问')),
                ('method', models.CharField(blank=True, choices=[('get', '获取'), ('post', '新增'), ('put', '更新'), ('delete', '删除')], max_length=50, null=True, verbose_name='操作行为/执行方法(针对api)')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='web_role', to='users.Role', verbose_name='角色id')),
            ],
            options={
                'verbose_name': '角色权限表',
                'verbose_name_plural': '角色权限表',
            },
        ),
        migrations.CreateModel(
            name='WebResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='权限名称')),
                ('path', models.CharField(blank=True, max_length=200, null=True, verbose_name='访问url')),
                ('is_menu', models.BooleanField(default=False, verbose_name='是否为菜单')),
                ('level', models.PositiveSmallIntegerField(choices=[(1, '模块'), (2, '子模块'), (3, 'api接口')], verbose_name='菜单级别')),
                ('sort', models.IntegerField(blank=True, default=100, null=True, verbose_name='排序')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.WebResource', verbose_name='父级权限')),
            ],
            options={
                'verbose_name': '菜单',
                'verbose_name_plural': '菜单',
            },
        ),
        migrations.AddField(
            model_name='roleresourceassign',
            name='webres',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_web', to='users.WebResource', verbose_name='模块id'),
        ),
        migrations.AddField(
            model_name='role',
            name='resource',
            field=models.ManyToManyField(through='users.RoleResourceAssign', to='users.WebResource', verbose_name='角色的用户'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='dept',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_dept', to='users.Organization', verbose_name='用户部门'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='org',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_org', to='users.Organization', verbose_name='用户组织'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_role', to='users.Role', verbose_name='用户角色'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together=set([('name', 'org')]),
        ),
    ]
