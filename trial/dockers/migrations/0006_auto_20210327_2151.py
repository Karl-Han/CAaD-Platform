# Generated by Django 3.1.6 on 2021-03-27 13:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dockers', '0005_auto_20210327_2149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='name',
            new_name='image_id',
        ),
        migrations.AlterField(
            model_name='instance',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 27, 13, 51, 5, 271336, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='instance',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 27, 13, 51, 5, 271407, tzinfo=utc), verbose_name='date last update'),
        ),
    ]
