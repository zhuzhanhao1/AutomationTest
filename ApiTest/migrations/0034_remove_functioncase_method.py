# Generated by Django 3.0.5 on 2020-05-29 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ApiTest', '0033_functioncase_functioncasechild'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='functioncase',
            name='method',
        ),
    ]