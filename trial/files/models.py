from django.db import models

from files.rfields import RestrictedFileField

# Create your models here.
class File(models.Model):
    # main info
    uid = models.IntegerField('user id')

    # status info
    create_date = models.DateTimeField('date created')

    # inherit
    class Meta:
        abstract = True

class FileHomework(File):
    hid = models.IntegerField('homework id')
    file = RestrictedFileField(upload_to='hw/%Y/%m/%d/', max_length=100, max_upload_size=5242880, 
            content_types=['application/pdf', 'application/excel', 'application/msword', 'text/plain', 'text/csv', 'application/zip', 'image/jpeg', 'image/gif', 'image/gif', 'image/bmp', 'image/tiff'])

class FileHomeworkStatu(File):
    hsid = models.IntegerField('homeworkStatu id')
    file = RestrictedFileField(upload_to='hs/%Y/%m/%d/', max_length=100, max_upload_size=5242880, 
            content_types=['application/pdf', 'application/excel', 'application/msword', 'text/plain', 'text/csv', 'application/zip', 'image/jpeg', 'image/gif', 'image/gif', 'image/bmp', 'image/tiff'])

