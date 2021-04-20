from django.db import models
from django.utils import timezone
from django.http import FileResponse, Http404

import time
import os

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
            content_types=['application/pdf', 'application/excel', 'application/msword', 'text/plain', 'text/csv', 'application/zip', 'image/jpeg', 'image/gif'])
    
    def __str__(self):
        return "SubmissionFile({}, {})".format(self.pk, self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            self.file_hash = hash(self.file.chunks())
            self.file.open()
            self.name = self.file.name
        print(self)

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def get_local_path(self):
        return self.file.path
    
    def delete(self, using=None, keep_parents=False):
        path = self.get_local_path()
        os.remove(path)
        return super().delete(using=using, keep_parents=keep_parents)

    @classmethod
    def get_file_response(cls, file_id):
        try:
            obj = cls.objects.get(pk=file_id)
            path = obj.get_local_path()
            response = FileResponse(open(path, "rb"), filename=obj.name)
            return response
        except cls.DoesNotExist:
            logger.error("No such file")
            return Http404("No such file")

class DockerFile(File):
    DOCKERFILE_STATUS = [(1, "To be review"), (2, "Reviewed"), (3, "Image built")]

    file = RestrictedFileField(upload_to=UploadToPathAndRename("dockerfile/" + time.strftime("%Y/%m/%d")), max_length=200, max_upload_size=5242880, 
            content_types=['application/zip'])
    status = models.IntegerField("dockerfile review status", choices=DOCKERFILE_STATUS, default=1)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            self.file_hash = hash(self.file.chunks())
            self.file.open()
            self.name = self.file.name
            self.content_type = "application/zip"

        print("update_fields in Dockerfile: {}".format(update_fields))

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

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
            return Http404("No such file")