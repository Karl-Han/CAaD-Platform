from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    # main info
    nickname = models.CharField('user name', max_length=32)
    password = models.CharField('maked password', max_length=128)
    email = models.CharField('email', max_length=128)

    # addition info
    avatar = models.CharField('avatar path', max_length=128)  # path + sha3_256 name(64)
    realname = models.CharField('real name', max_length=16)
    uid = models.CharField('user(student/teacher) number', max_length=32)

    # status info
    #privilege = ( (0, 'admin_public'), (1, 'reserved'), (2, 'reserved'), (3, 'reserved'), (4, 'reserved'), (5, 'normal') )
    privilege = models.IntegerField('privilege')
    #status = ( (0, 'unactivated'), (1, 'normal'), (2, 'banned'), (3, 'canceled'),  )
    status = models.IntegerField('user status')
    signup_date = models.DateTimeField('date signed up')

    # login info
    last_login = models.DateTimeField('last login')
    token = models.CharField('login token', max_length=128)  # sha3_512, name 'utk' in frontend cookies
    counter = models.DateTimeField('counter (multiple use)', default=timezone.now().now())


