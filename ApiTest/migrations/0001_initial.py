# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-12-13 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('caseid', models.AutoField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('casename', models.CharField(max_length=100, verbose_name='用例名称')),
                ('identity', models.CharField(max_length=50, verbose_name='用户身份')),
                ('url', models.CharField(max_length=250, verbose_name='访问路径')),
                ('method', models.CharField(max_length=20, verbose_name='请求方式')),
                ('header', models.CharField(max_length=200, verbose_name='请求头')),
                ('params', models.TextField(verbose_name='请求参数')),
                ('body', models.TextField(verbose_name='请求体内容')),
                ('exceptres', models.TextField(verbose_name='期望结果')),
                ('result', models.TextField(verbose_name='执行结果')),
                ('belong', models.CharField(max_length=50, verbose_name='所属模块')),
                ('system', models.CharField(max_length=50, verbose_name='所属系统')),
                ('sortid', models.IntegerField(verbose_name='排序号')),
                ('duration', models.FloatField(verbose_name='响应时长')),
                ('head', models.CharField(max_length=200, verbose_name='负责人')),
            ],
        ),
    ]
