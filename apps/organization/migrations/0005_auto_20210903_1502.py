# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2021-09-03 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='全国知名', max_length=10, verbose_name='机构标签'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='teacher_age',
            field=models.IntegerField(default=20, verbose_name='年龄'),
        ),
    ]
