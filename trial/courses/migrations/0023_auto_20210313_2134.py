# Generated by Django 3.1.6 on 2021-03-13 13:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0022_auto_20210313_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 13, 34, 52, 374777, tzinfo=utc), verbose_name='date created up'),
        ),
    ]
