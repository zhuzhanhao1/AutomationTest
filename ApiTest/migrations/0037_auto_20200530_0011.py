# Generated by Django 3.0.5 on 2020-05-29 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiTest', '0036_auto_20200529_2335'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='functioncasechild',
            options={'verbose_name': '用例管理子表', 'verbose_name_plural': '功能用例管理子表'},
        ),
        migrations.AddField(
            model_name='functioncasechild',
            name='step_id',
            field=models.CharField(default=1, max_length=10, verbose_name='步骤序号'),
            preserve_default=False,
        ),
    ]
