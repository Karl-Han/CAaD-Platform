from django.db import models

# Create your models here.
class Homework(models.Model):
    # main info
    title = models.CharField('title', max_length=64)
    description = models.CharField('description', max_length=1024)
    cid = models.IntegerField('course id')
    ctrid = models.IntegerField('creater user id')
    tips = models.CharField('tips', max_length=1024)
    answer = models.CharField('answer', max_length=1024)
    dockerAPI = models.CharField('dockerAPI', max_length=128)  # reserved

    # status info
    #status = ( (0, 'draft'), (1, 'running'), (2, 'closed') )
    status = models.IntegerField('homework status')
    #types = ( (0, 'reserved') )
    types = models.IntegerField('homework types')
    create_date = models.DateTimeField('date created')
    close_date = models.DateTimeField('date to close')

class HomeworkStatu(models.Model):
    cid = models.IntegerField('course id')
    uid = models.IntegerField('user id')
    hid = models.IntegerField('homework id')

    grades = models.IntegerField('grades')
    comment = models.CharField('comment', max_length=1024)

    #status = ( (0, 'manager?(reserved)'), (1, 'undo&intime'), (2, 'done&intime'), (3, 'undo&timeout'), (4, 'done&timeout') )
    status = models.IntegerField('status')

