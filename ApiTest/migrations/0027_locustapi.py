# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-15 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiTest', '0026_systemrole_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocustApi',
            fields=[
                ('caseid', models.AutoField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('identity', models.CharField(max_length=50, verbose_name='用户身份')),
                ('url', models.CharField(max_length=250, verbose_name='访问路径')),
                ('method', models.CharField(max_length=20, verbose_name='请求方式')),
                ('header', models.CharField(blank=True, max_length=200, null=True, verbose_name='请求头')),
                ('params', models.TextField(blank=True, null=True, verbose_name='请求参数')),
                ('body', models.TextField(blank=True, null=True, verbose_name='请求体内容')),
                ('ip', models.CharField(max_length=100, verbose_name='ip地址')),
            ],
            options={
                'verbose_name': '接口性能测试',
                'verbose_name_plural': '接口性能测试',
            },
        ),
    ]
