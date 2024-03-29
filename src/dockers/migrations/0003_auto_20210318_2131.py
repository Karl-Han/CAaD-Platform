# Generated by Django 3.1.6 on 2021-03-18 13:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dockers', '0002_auto_20210318_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 13, 31, 21, 557435, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='instance',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 13, 31, 21, 557467, tzinfo=utc), verbose_name='date last update'),
        ),
    ]
