# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-12-14 15:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ApiTest', '0005_auto_20191214_2331'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ApiCase',
            new_name='SingleApi',
        ),
    ]
