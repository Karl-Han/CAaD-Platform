# Generated by Django 3.1.6 on 2021-03-16 08:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0030_auto_20210316_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 16, 8, 50, 37, 162134, tzinfo=utc), verbose_name='date created up'),
        ),
    ]