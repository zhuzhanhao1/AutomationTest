# Generated by Django 3.0.5 on 2020-05-29 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiTest', '0035_auto_20200529_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='functioncase',
            name='executor',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='执行人'),
        ),
        migrations.AlterField(
            model_name='functioncase',
            name='note',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='备注'),
        ),
    ]
