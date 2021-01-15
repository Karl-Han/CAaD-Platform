# Generated by Django 3.1.4 on 2021-01-14 08:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=32, verbose_name='user name')),
                ('password', models.CharField(max_length=128, verbose_name='maked password')),
                ('email', models.CharField(max_length=128, verbose_name='email')),
                ('avatar', models.CharField(max_length=128, verbose_name='avatar path')),
                ('realname', models.CharField(max_length=16, verbose_name='real name')),
                ('uid', models.CharField(max_length=32, verbose_name='user(student/teacher) number')),
                ('privilege', models.IntegerField(verbose_name='privilege')),
                ('status', models.IntegerField(verbose_name='user status')),
                ('signup_date', models.DateTimeField(verbose_name='date signed up')),
                ('last_login', models.DateTimeField(verbose_name='last login')),
                ('token', models.CharField(max_length=128, verbose_name='login token')),
                ('counter', models.DateTimeField(default=datetime.datetime(2021, 1, 14, 8, 13, 58, 262790), verbose_name='counter (multiple use)')),
            ],
        ),
    ]
