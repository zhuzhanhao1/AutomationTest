# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-12-15 05:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ApiTest', '0006_auto_20191214_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeftMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('area', models.CharField(max_length=150, verbose_name='区域')),
                ('title', models.CharField(max_length=150, verbose_name='标题')),
                ('icon', models.CharField(default='&#xe674', max_length=150, verbose_name='图标')),
                ('href', models.CharField(max_length=150, verbose_name='链接')),
                ('spread', models.BooleanField(default=False, verbose_name='默认不展开')),
                ('children', models.TextField(default=[], verbose_name='子菜单')),
            ],
            options={
                'verbose_name': '左侧菜单',
                'verbose_name_plural': '左侧菜单管理',
            },
        ),
        migrations.AlterModelOptions(
            name='automenu',
            options={'verbose_name': '二级菜单', 'verbose_name_plural': '二级菜单管理'},
        ),
        migrations.AlterField(
            model_name='automenu',
            name='classification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='分类', to='ApiTest.LeftMenu', verbose_name='所属分类'),
        ),
        migrations.AlterField(
            model_name='automenu',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
