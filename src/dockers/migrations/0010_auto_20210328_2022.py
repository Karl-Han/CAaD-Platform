# Generated by Django 3.1.6 on 2021-03-28 12:22

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0026_auto_20210328_2022'),
        ('dockers', '0009_auto_20210328_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='homeworks.task'),
        ),
        migrations.AlterField(
            model_name='instance',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 12, 22, 36, 608765, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='instance',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 12, 22, 36, 608793, tzinfo=utc), verbose_name='date last update'),
        ),
    ]
