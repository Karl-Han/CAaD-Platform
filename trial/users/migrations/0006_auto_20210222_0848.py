# Generated by Django 3.1.6 on 2021-02-22 08:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210222_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='counter',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 22, 8, 48, 53, 51108), verbose_name='counter (multiple use)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='signup_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 22, 8, 48, 53, 51038), verbose_name='date signed up'),
        ),
    ]
