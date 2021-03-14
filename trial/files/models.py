from django.db import models
from django.utils import timezone
from django.http import FileResponse, Http404

import time

from trial.views import logger
from .rfields import RestrictedFileField
from .utils import hash, UploadToPathAndRename

class File(models.Model):
    name = models.CharField(max_length=32, blank=True)
    create_date = models.DateTimeField('date created', default=timezone.now())
    hash = models.CharField(max_length=64, blank=True)
    content_type = models.CharField(max_length=64, blank=True, null=True)

    # inherit
    class Meta:
        abstract = True

class SubmissionFile(File):
    file = RestrictedFileField(upload_to=UploadToPathAndRename("submission/" + time.strftime("%Y/%m/%d")), max_length=100, max_upload_size=5242880, 
            content_types=['application/pdf', 'application/excel', 'application/msword', 'text/plain', 'text/csv', 'application/zip', 'image/jpeg', 'image/gif', 'image/gif', 'image/bmp', 'image/tiff'])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.file_hash = hash(self.file.chunks())
        self.file.open()
        self.name = self.file.name
        self.content_type = self.file.content_type

        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def get_local_path(self):
        return self.file.path

    @classmethod
    def get_file_response(cls, file_id):
        try:
            obj = cls.objects.get(pk=file_id)
            path = obj.get_local_path()
            response = FileResponse(open(path, "rb"))
            return response
        except cls.DoesNotExist:
            logger.error("No such file")
            Http404("No such file")