# Generated by Django 3.1.6 on 2021-03-18 13:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0017_auto_20210317_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='docker_api',
        ),
        migrations.AddField(
            model_name='task',
            name='have_docker',
            field=models.BooleanField(default=False, verbose_name='have docker experiment'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='commit_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 13, 31, 18, 822389, tzinfo=utc), verbose_name='date committed'),
        ),
        migrations.AlterField(
            model_name='task',
            name='close_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 17, 13, 31, 18, 821666, tzinfo=utc), verbose_name='date to close'),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 13, 31, 18, 821645, tzinfo=utc), verbose_name='date created'),
        ),
    ]
