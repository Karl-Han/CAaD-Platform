# Generated by Django 3.1.6 on 2021-03-28 12:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0025_auto_20210328_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='commit_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 12, 22, 36, 519917, tzinfo=utc), verbose_name='date committed'),
        ),
        migrations.AlterField(
            model_name='task',
            name='close_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 27, 12, 22, 36, 519199, tzinfo=utc), verbose_name='date to close'),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 12, 22, 36, 519159, tzinfo=utc), verbose_name='date created'),
        ),
    ]
