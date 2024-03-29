# Generated by Django 3.1.6 on 2021-04-06 07:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import files.rfields
import files.utils


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0024_auto_20210328_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockerfile',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 7, 5, 37, 804599, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='dockerfile',
            name='file',
            field=files.rfields.RestrictedFileField(upload_to=files.utils.UploadToPathAndRename('dockerfile/2021/04/06')),
        ),
        migrations.AlterField(
            model_name='submissionfile',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 7, 5, 37, 804599, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='submissionfile',
            name='file',
            field=files.rfields.RestrictedFileField(upload_to=files.utils.UploadToPathAndRename('submission/2021/04/06')),
        ),
    ]
