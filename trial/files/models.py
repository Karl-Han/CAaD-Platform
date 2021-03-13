from django.db import models
from django.utils import timezone

import time

from .rfields import RestrictedFileField
from .utils import hash, UploadToPathAndRename

class File(models.Model):
    file_name = models.CharField(max_length=32, blank=True)
    create_date = models.DateTimeField('date created', default=timezone.now())
    file_hash = models.CharField(max_length=64, blank=True)

    # inherit
    class Meta:
        abstract = True

class SubmissionFile(File):
    file = RestrictedFileField(upload_to=UploadToPathAndRename(time.strftime("%Y/%m/%d")), max_length=100, max_upload_size=5242880, 
            content_types=['application/pdf', 'application/excel', 'application/msword', 'text/plain', 'text/csv', 'application/zip', 'image/jpeg', 'image/gif', 'image/gif', 'image/bmp', 'image/tiff'])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # print(self.file.name)
        self.file_hash = hash(self.file.chunks())
        self.file.open()
        self.file_name = self.file.name
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

# class FileHomeworkStatu(File):
#     hsid = models.IntegerField('homeworkStatu id')
#     file = RestrictedFileField(upload_to='hs/%Y/%m/%d/', max_length=100, max_upload_size=5242880, 
#             content_types=['application/pdf', 'application/excel', 'application/msword', 'text/plain', 'text/csv', 'application/zip', 'image/jpeg', 'image/gif', 'image/gif', 'image/bmp', 'image/tiff'])
# 
# class FileDocker(File):
#     hid = models.IntegerField('homework id')
#     file = RestrictedFileField(upload_to='docker/',     # default name: hid
#             max_length=100, max_upload_size=104857600,  # enough?
#             content_types=['application/zip'])          # TODO: more types