# Generated by Django 3.1.6 on 2021-03-27 13:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0035_auto_20210318_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 27, 13, 49, 47, 53583, tzinfo=utc), verbose_name='date created up'),
        ),
        migrations.AlterField(
            model_name='coursemember',
            name='type',
            field=models.IntegerField(choices=[(0, 'admin'), (1, 'teacher'), (2, 'assistant'), (3, 'student')], verbose_name='Member type'),
        ),
    ]