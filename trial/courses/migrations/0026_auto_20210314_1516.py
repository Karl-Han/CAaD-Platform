# Generated by Django 3.1.6 on 2021-03-14 07:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0025_auto_20210313_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 14, 7, 16, 3, 322011, tzinfo=utc), verbose_name='date created up'),
        ),
    ]
