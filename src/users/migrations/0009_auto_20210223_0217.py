# Generated by Django 3.1.6 on 2021-02-23 02:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210223_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='counter',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 23, 2, 17, 29, 858195), verbose_name='counter (multiple use)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='signup_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 23, 2, 17, 29, 858130), verbose_name='date signed up'),
        ),
    ]