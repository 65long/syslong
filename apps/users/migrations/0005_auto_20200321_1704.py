# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-03-21 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200321_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webresource',
            name='component',
            field=models.CharField(default='login/Login', max_length=300, verbose_name='前端组件'),
        ),
    ]
