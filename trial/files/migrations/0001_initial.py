# Generated by Django 3.1.4 on 2021-02-11 10:31

from django.db import migrations, models
import files.rfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileHomework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(verbose_name='user id')),
                ('create_date', models.DateTimeField(verbose_name='date created')),
                ('hid', models.IntegerField(verbose_name='homework id')),
                ('file', files.rfields.RestrictedFileField(upload_to='hw/%Y/%m/%d/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FileHomeworkStatu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(verbose_name='user id')),
                ('create_date', models.DateTimeField(verbose_name='date created')),
                ('hsid', models.IntegerField(verbose_name='homeworkStatu id')),
                ('file', files.rfields.RestrictedFileField(upload_to='hs/%Y/%m/%d/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
