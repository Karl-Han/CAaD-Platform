# Generated by Django 3.1.6 on 2021-02-22 15:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210222_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, max_length=128, verbose_name='avatar path'),
        ),
        migrations.AlterField(
            model_name='user',
            name='counter',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 22, 15, 28, 58, 11804), verbose_name='counter (multiple use)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='realname',
            field=models.CharField(blank=True, max_length=16, verbose_name='real name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='signup_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 22, 15, 28, 58, 11742), verbose_name='date signed up'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.CharField(blank=True, max_length=32, verbose_name='user(student/teacher) number'),
        ),
    ]
