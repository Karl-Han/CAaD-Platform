# Generated by Django 3.1.6 on 2021-03-08 13:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20210308_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 13, 41, 5, 257465, tzinfo=utc), verbose_name='date created up'),
        ),
    ]
