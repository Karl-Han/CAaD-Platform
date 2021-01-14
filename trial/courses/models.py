from django.db import models

# Create your models here.
class Course(models.Model):
    # main info
    name = models.CharField('user name', max_length=32)
    password = models.CharField('password for joining', max_length=8)  # digits and upper char (generate randomly)

    # addition info
    ctrid = models.IntegerField('creater user id')
    description = models.CharField('description', max_length=512)

    # status info
    #status = ( (0, 'to be activate'), (1, 'unstarted'), (2, 'running'), (3, 'finished') )
    status = models.IntegerField('course status')
    types = models.IntegerField('course types')  # reserved
    create_date = models.DateTimeField('date created up')
    hot = models.IntegerField('hot')  # for recommending

class CourseMember(models.Model):
    cid = models.IntegerField('course id')
    uid = models.IntegerField('member user id')
    #type = ( (0, 'admin'), (1, 'teacher'), (2, 'asistant'), (3, 'student'), (4, visistor) )
    types = models.IntegerField('user type (privilege)')
