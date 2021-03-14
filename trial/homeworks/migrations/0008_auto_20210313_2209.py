# Generated by Django 3.1.6 on 2021-03-13 14:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0007_auto_20210313_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='commit_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 14, 9, 31, 703822, tzinfo=utc), verbose_name='date committed'),
        ),
        migrations.AlterField(
            model_name='task',
            name='close_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 12, 14, 9, 31, 703050, tzinfo=utc), verbose_name='date to close'),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 14, 9, 31, 703028, tzinfo=utc), verbose_name='date created'),
        ),
    ]