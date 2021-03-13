import os
import types
from trial.views import logger
from Crypto.Hash import SHA3_256

from django.utils.deconstruct import deconstructible

def hash(file):
    if file:
        hasher = SHA3_256.new()
        if not isinstance(file, types.GeneratorType):
            hasher.update(file)
        else:
            for chunk in file:
                hasher.update(chunk)
        return str(hasher.digest())

    raise IOError("No file hander")

@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.file:
            # file exist
            filename = hash(instance.file.read())
        else:
            logger.error("Unable to read file.")
            raise IOError("No such file in the instance") 
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)