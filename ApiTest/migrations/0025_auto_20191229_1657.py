# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-12-29 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiTest', '0024_auto_20191229_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processapi',
            name='belong',
            field=models.CharField(default='', max_length=200, verbose_name='所属模块'),
            preserve_default=False,
        ),
    ]