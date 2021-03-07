# Generated by Django 3.1.4 on 2021-02-11 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='user name')),
                ('password', models.CharField(max_length=8, verbose_name='password for joining')),
                ('ctrid', models.IntegerField(verbose_name='creater user id')),
                ('description', models.CharField(max_length=512, verbose_name='description')),
                ('status', models.IntegerField(verbose_name='course status')),
                ('types', models.IntegerField(verbose_name='course types')),
                ('create_date', models.DateTimeField(verbose_name='date created up')),
                ('popularity', models.IntegerField(verbose_name='popularity')),
            ],
        ),
        migrations.CreateModel(
            name='CourseMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.IntegerField(verbose_name='course id')),
                ('uid', models.IntegerField(verbose_name='member user id')),
                ('types', models.IntegerField(verbose_name='user type (privilege)')),
            ],
        ),
    ]
