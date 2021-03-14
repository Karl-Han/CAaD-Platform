# Generated by Django 3.1.6 on 2021-03-10 12:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0003_auto_20210310_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='close_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 9, 12, 15, 33, 218146, tzinfo=utc), verbose_name='date to close'),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 10, 12, 15, 33, 218124, tzinfo=utc), verbose_name='date created'),
        ),
    ]