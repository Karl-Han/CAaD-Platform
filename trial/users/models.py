from django.db import models
from django.utils import timezone

import datetime

# Create your models here.


class User(models.Model):
    PRIVILEGE = [
        (0, 'admin_public'),
        (1, 'reserved'),
        (2, 'reserved'),
        (3, 'reserved'),
        (4, 'reserved'),
        (5, 'normal')
    ]

    USER_STATUS = [
        (0, 'unactivated'), 
        (1, 'normal'),
        (2, 'banned'), 
        (3, 'canceled'), 
    ]

    # main info
    nickname = models.CharField('user name', max_length=32, unique=True)
    email = models.EmailField('email', unique=True)
    password = models.CharField('maked password', max_length=128)
    signup_date = models.DateTimeField('date signed up', default=datetime.datetime.now())

    # login info
    last_login = models.DateTimeField('last login', default=datetime.datetime(2021, 2, 22))
    # sha3_512, name 'utk' in frontend cookies
    token = models.CharField('login token', max_length=128, null=True)
    counter = models.DateTimeField(
        'counter (multiple use)', default=timezone.now().now())

    # status info
    privilege = models.IntegerField(
        choices=PRIVILEGE, verbose_name='User Privilege', default=5)
    status = models.IntegerField(choices=USER_STATUS, verbose_name='User Status', default=0)

    # addition info
    # path + sha3_256 name(64)
    avatar = models.CharField('avatar path', max_length=128, blank=True)
    realname = models.CharField('real name', max_length=16, blank=True)
    uid = models.CharField('user(student/teacher) number', max_length=32, blank=True)

    def __str__(self):
        return "<Student: {}".format(self.nickname)

    class Meta:
        verbose_name = verbose_name_plural = "User information"