# Generated by Django 3.1.6 on 2021-04-06 07:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0025_auto_20210406_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockerfile',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 7, 7, 15, 157810, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='submissionfile',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 7, 7, 15, 157810, tzinfo=utc), verbose_name='date created'),
        ),
    ]
