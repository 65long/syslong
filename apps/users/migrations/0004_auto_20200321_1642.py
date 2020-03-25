# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-03-21 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200318_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='webresource',
            name='component',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='前端组件'),
        ),
        migrations.AddField(
            model_name='webresource',
            name='icon',
            field=models.CharField(default='tree-table', max_length=100, verbose_name='前端图标'),
        ),
    ]