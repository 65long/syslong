# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-09-20 15:44
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200920_1543'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RoleGroup',
        ),
        migrations.AlterField(
            model_name='organization',
            name='code_link',
            field=models.CharField(default=uuid.UUID('6b219c0a-6975-409e-ba26-a939edb26b58'), max_length=2000, verbose_name='快查链接'),
        ),
    ]
