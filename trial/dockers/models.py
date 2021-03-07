from django.db import models

# Create your models here.
class DockerStatu(models.Model):
    # main info
    ctrid = models.IntegerField('creater user id')
    hid = models.IntegerField('homework id')

    # docker info
    name = models.CharField('tag name', max_length=32)  # maybe hid, reserved
    ctnid = models.CharField('container id', max_length=64)
    imgid = models.CharField('image id', max_length=64)
    iport = models.IntegerField('port in container')
    oport = models.IntegerField('port in server')

    # status info
    #types = ( (0, 'reserved') )
    types = models.IntegerField('types')
    #status = ( (0, 'none'), (1, 'creatting'), (2, 'fail'), (3, 'running'), (4, updating), (5, deling) )
    status = models.IntegerField('status')
    create_date = models.DateTimeField('date created')
    update_date = models.DateTimeField('date last update')

