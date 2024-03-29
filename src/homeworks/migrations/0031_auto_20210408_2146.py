# Generated by Django 3.1.6 on 2021-04-08 13:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0029_auto_20210408_2146'),
        ('homeworks', '0030_auto_20210408_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='dockerfile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.dockerfile'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='commit_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 8, 13, 46, 24, 345956, tzinfo=utc), verbose_name='date committed'),
        ),
        migrations.AlterField(
            model_name='task',
            name='close_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 8, 13, 46, 24, 345252, tzinfo=utc), verbose_name='date to close'),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 8, 13, 46, 24, 345225, tzinfo=utc), verbose_name='date created'),
        ),
    ]
