# Generated by Django 3.1.6 on 2021-04-08 03:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0043_auto_20210406_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 8, 3, 12, 26, 293524, tzinfo=utc), verbose_name='date created up'),
        ),
    ]
