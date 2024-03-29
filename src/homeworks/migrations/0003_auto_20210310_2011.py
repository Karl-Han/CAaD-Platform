# Generated by Django 3.1.6 on 2021-03-10 12:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0002_filedocker'),
        ('courses', '0018_auto_20210310_2011'),
        ('homeworks', '0002_auto_20210310_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='file_id',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='task_id',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='creator_id',
        ),
        migrations.AddField(
            model_name='submission',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='courses.course'),
        ),
        migrations.AddField(
            model_name='submission',
            name='file',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='files.filehomework'),
        ),
        migrations.AddField(
            model_name='submission',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='homeworks.task'),
        ),
        migrations.AddField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='courses.course'),
        ),
        migrations.AddField(
            model_name='task',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='close_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 9, 12, 11, 45, 177503, tzinfo=utc), verbose_name='date to close'),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 10, 12, 11, 45, 177481, tzinfo=utc), verbose_name='date created'),
        ),
    ]
