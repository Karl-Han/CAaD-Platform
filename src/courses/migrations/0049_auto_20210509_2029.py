# Generated by Django 3.1.6 on 2021-05-09 12:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0048_auto_20210409_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 9, 12, 29, 26, 52632, tzinfo=utc), verbose_name='date created up'),
        ),
    ]
