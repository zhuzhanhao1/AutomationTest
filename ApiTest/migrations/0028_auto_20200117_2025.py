# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-17 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiTest', '0027_locustapi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemrole',
            name='ip',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='IP地址'),
        ),
    ]