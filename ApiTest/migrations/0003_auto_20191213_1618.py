# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-12-13 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiTest', '0002_auto_20191213_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apicase',
            name='sortid',
            field=models.IntegerField(default=1, verbose_name='排序号'),
        ),
        migrations.AlterField(
            model_name='apicase',
            name='system',
            field=models.CharField(default='erms', max_length=50, verbose_name='所属系统'),
        ),
    ]
