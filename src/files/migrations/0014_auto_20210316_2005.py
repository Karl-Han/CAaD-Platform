# Generated by Django 3.1.6 on 2021-03-16 12:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0013_auto_20210316_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionfile',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 16, 12, 5, 6, 459885, tzinfo=utc), verbose_name='date created'),
        ),
    ]
