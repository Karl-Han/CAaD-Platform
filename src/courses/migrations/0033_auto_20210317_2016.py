# Generated by Django 3.1.6 on 2021-03-17 12:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0032_auto_20210316_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 17, 12, 16, 53, 700443, tzinfo=utc), verbose_name='date created up'),
        ),
    ]
