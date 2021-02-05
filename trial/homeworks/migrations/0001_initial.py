# Generated by Django 3.1.4 on 2021-02-05 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('description', models.CharField(max_length=1024, verbose_name='description')),
                ('cid', models.IntegerField(verbose_name='course id')),
                ('ctrid', models.IntegerField(verbose_name='creater user id')),
                ('tips', models.CharField(max_length=1024, verbose_name='tips')),
                ('answer', models.CharField(max_length=1024, verbose_name='answer')),
                ('dockerAPI', models.CharField(max_length=128, verbose_name='dockerAPI')),
                ('status', models.IntegerField(verbose_name='homework status')),
                ('types', models.IntegerField(verbose_name='homework types')),
                ('create_date', models.DateTimeField(verbose_name='date created')),
                ('close_date', models.DateTimeField(verbose_name='date to close')),
            ],
        ),
        migrations.CreateModel(
            name='HomeworkStatu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.IntegerField(verbose_name='course id')),
                ('uid', models.IntegerField(verbose_name='user id')),
                ('hid', models.IntegerField(verbose_name='homework id')),
                ('grades', models.IntegerField(verbose_name='grades')),
                ('comment', models.CharField(max_length=1024, verbose_name='comment')),
                ('status', models.IntegerField(verbose_name='status')),
            ],
        ),
    ]
