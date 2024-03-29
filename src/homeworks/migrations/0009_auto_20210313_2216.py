# Generated by Django 3.1.6 on 2021-03-13 14:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0006_submissionfile'),
        ('homeworks', '0008_auto_20210313_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='commit_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 14, 16, 2, 740223, tzinfo=utc), verbose_name='date committed'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='file',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submission', to='files.submissionfile'),
        ),
        migrations.AlterField(
            model_name='task',
            name='close_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 12, 14, 16, 2, 739296, tzinfo=utc), verbose_name='date to close'),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 14, 16, 2, 739272, tzinfo=utc), verbose_name='date created'),
        ),
    ]
