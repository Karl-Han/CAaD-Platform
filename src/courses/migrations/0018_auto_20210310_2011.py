# Generated by Django 3.1.6 on 2021-03-10 12:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_auto_20210310_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 10, 12, 11, 45, 171995, tzinfo=utc), verbose_name='date created up'),
        ),
    ]
