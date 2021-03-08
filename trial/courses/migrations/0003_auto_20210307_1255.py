# Generated by Django 3.1.6 on 2021-03-07 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_auto_20210222_0326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursemember',
            old_name='types',
            new_name='type',
        ),
        migrations.RemoveField(
            model_name='course',
            name='ctrid',
        ),
        migrations.RemoveField(
            model_name='course',
            name='popularity',
        ),
        migrations.RemoveField(
            model_name='course',
            name='status',
        ),
        migrations.RemoveField(
            model_name='course',
            name='types',
        ),
        migrations.RemoveField(
            model_name='coursemember',
            name='cid',
        ),
        migrations.RemoveField(
            model_name='coursemember',
            name='uid',
        ),
        migrations.AddField(
            model_name='course',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coursemember',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='coursemember',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=32, verbose_name='course name'),
        ),
        migrations.AlterField(
            model_name='course',
            name='password',
            field=models.CharField(max_length=8, verbose_name='joining password'),
        ),
    ]
