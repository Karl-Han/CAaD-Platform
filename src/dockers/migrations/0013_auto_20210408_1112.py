# Generated by Django 3.1.6 on 2021-04-08 03:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dockers', '0012_auto_20210406_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='status',
            field=models.IntegerField(choices=[(0, 'creating'), (1, 'running'), (2, 'stopped'), (3, 'deleted')], default=3, verbose_name='container status'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='instance',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 8, 3, 12, 26, 394738, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='instance',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 8, 3, 12, 26, 394766, tzinfo=utc), verbose_name='date last update'),
        ),
    ]
