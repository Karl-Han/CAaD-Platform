# Generated by Django 3.1.6 on 2021-03-27 13:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import files.rfields
import files.utils


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0018_auto_20210318_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockerfile',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 27, 13, 49, 47, 65955, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='dockerfile',
            name='file',
            field=files.rfields.RestrictedFileField(upload_to=files.utils.UploadToPathAndRename('dockerfile/2021/03/27')),
        ),
        migrations.AlterField(
            model_name='submissionfile',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 27, 13, 49, 47, 65955, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='submissionfile',
            name='file',
            field=files.rfields.RestrictedFileField(upload_to=files.utils.UploadToPathAndRename('submission/2021/03/27')),
        ),
    ]
