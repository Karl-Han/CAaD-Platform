from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import datetime

# Create your models here.


class UserAuxiliary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="auxiliary", unique=True)

    # avatar = models.CharField('avatar path', max_length=128, blank=True)
    realname = models.CharField('real name', max_length=16, blank=True, null=True)
    uid = models.CharField('user(student/teacher) number', max_length=32, blank=True, null=True)

    def __str__(self):
        return "<User: {}".format(self.user.username)

    class Meta:
        verbose_name = verbose_name_plural = "User auxiliary information"