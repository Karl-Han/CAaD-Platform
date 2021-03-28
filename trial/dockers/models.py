from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

import os
import docker
import json
import shutil
import time

from files.models import DockerFile
from homeworks.models import Task, Submission
from utils.params import DOCKER_BASE_URL
from .utils import unzip, get_docker_client, get_rand_available_port

class Image(models.Model):
    image_id = models.CharField("image id", max_length=64, null=True)
    port_open = models.IntegerField("open port", null=True)
    dockerfile = models.OneToOneField(DockerFile, on_delete=models.CASCADE)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="image")

    def build_image(self):
        # Unzip file to media/docker/<task_id>
        file_path = self.dockerfile.get_local_path()
        dst = os.path.join(settings.MEDIA_ROOT, "docker", str(self.task.pk))
        print(dst)
        if not os.path.exists(dst):
            os.makedirs(dst)
        else:
            # os.removedirs(dst)
            shutil.rmtree(dst)
            os.makedirs(dst)
        unzip(file_path, dst)

        client = get_docker_client()
        res = []
        try:
            image, response = client.images.build(path=dst, rm=True, tag=self.task.pk)
            for r in response:
                res.append(r['stream'])
            print("res = {}".format(res))
        except Exception as e:
            print("Error: {}".format(e))
            # return False

        if not 'Successful' in str(res[-1]) and not 'cache' in str(res[-2]):
            # Clean the build and stop
            print("".join(res))
            raise Exception("Error when building image.")

        # Successfully built
        self.image_id = str(self.task.pk)
        self.dockerfile.status = 3
        self.dockerfile.save()
        self.save()
        print("Successfully built")

        return True

    def run_new_container(self, submission_id):
        submission = Submission.objects.get(pk=submission_id)
        client = get_docker_client()

        # Find port and run container
        port_server = get_rand_available_port()
        container = client.containers.run(self.image_id , detach=True,
            ports={ self.port_open:port_server})

        if container.status == "created":
            time.sleep(2)
            container = client.containers.get(container.id)
        if container.status != "running":
            # Not running properly
            raise Exception("Container is not running properly: ({}){}".format(container.id, container.status))

        # Finally record this container
        instance = Instance(container_id=container.id, image=self, 
            port_local=self.port_open, port_server=port_server,
            submission=submission)
        instance.save()
        return container.id, port_server


class Instance(models.Model):
    # CONTAINER_STATUS = [ (0, 'creating'), (1, 'running'), (2, 'stopped'), (3, 'deleted')]

    container_id = models.CharField('container id', max_length=64)
    port_local = models.IntegerField('port open in container')
    port_server = models.IntegerField('port allocated on server')

    create_date = models.DateTimeField('date created', default=timezone.now())
    update_date = models.DateTimeField('date last update', default=timezone.now())
    # status = models.IntegerField('container status', choices=CONTAINER_STATUS)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name="instance")

    def get_server_port(self):
        return self.port_server

    def delete(self, *args, **kwargs):
        # Clean up container first
        client = get_docker_client()
        try:
            container = client.containers.get(self.container_id)
            container.stop()
            container.remove()
        except:
            # No such container
            print("No such container({})".format(self.container_id))
        return super(Instance, self).delete(*args, **kwargs)

@receiver(post_save, sender=DockerFile)
def update_image_status(sender, **kwargs):
    instance = kwargs.pop("instance")
    created = kwargs.pop("created")
    update_fields = kwargs.pop("update_fields")
    # print("{}\n{}\n{}".format(instance, created, update_fields))

    status = False
    if not created:
        if update_fields is None or "status" not in update_fields:
            return False

        if instance.status == 2:
            print("Building image")
            status = instance.image.build_image()

        print(sender)
        return status