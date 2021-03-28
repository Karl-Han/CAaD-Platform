from django.db import models
from django.utils import timezone

import os
import docker

from files.models import DockerFile
from homeworks.models import Task, Submission
from utils.params import DOCKER_BASE_URL
from .utils import unzip, get_docker_client

class Image(models.Model):
    image_id = models.CharField("image id", max_length=64, null=True)
    port_open = models.IntegerField("open port", null=True)
    dockerfile = models.OneToOneField(DockerFile, on_delete=models.CASCADE)
    task = models.OneToOneField(Task, on_delete=models.CASCADE)

    def build_image(self):
        # Unzip file to media/docker/<task_id>
        file_path = self.dockerfile.get_local_path()
        dst = os.path.join(MEDIA_ROOT, "docker", self.task.pk)
        print(dst)
        if not os.path.exists(dst):
            os.makedirs(dst)
        else:
            os.removedirs(p)
            os.makedirs(p)
        unzip(file_path, dst)

        client = get_docker_client()
        try:
            image, response = client.build(path=dst, rm=True, tag=self.task.pk)
            print(response)
        except e:
            print(e)
            return False

        if not 'Successful' in str(response[-1]):
            # Clean the build and stop
            error_msg = []
            for msg in response:
                for v in json.loads(msg).values():
                    error_msg.append(v)
            print("".join(error_msg))
            raise Exception("Error when building image.")

        # Successfully built
        self.image_id = str(self.task.pk)
        self.dockerfile.status = 3
        self.save()
        return True

    def run_new_container(self, submission_id):
        submission = Submission.objects.get(pk=submission_id)
        client = get_docker_client()

        # Find port and run container
        port_server = get_rand_available_port()
        container = client.containers.run(self.image_id , detach=True,
            ports={ self.port_open:port_server})
        if container.status != "running":
            # Not running properly
            raise Exception("Container is not running properly: ({}){}".format(container.id, container.status))

        # Finally record this container
        instance = Instance(container_id=container.id, image=self, 
            port_local=self.port_open, port_server=port_server,
            submission=submission)
        instance.save()
        return True


class Instance(models.Model):
    # CONTAINER_STATUS = [ (0, 'creating'), (1, 'running'), (2, 'stopped'), (3, 'deleted')]

    container_id = models.CharField('container id', max_length=64)
    port_local = models.IntegerField('port open in container')
    port_server = models.IntegerField('port allocated on server')

    create_date = models.DateTimeField('date created', default=timezone.now())
    update_date = models.DateTimeField('date last update', default=timezone.now())
    # status = models.IntegerField('container status', choices=CONTAINER_STATUS)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)

    def get_server_port(self):
        return self.port_server

    def delete(self, *args, **kwargs):
        # Clean up container first
        client = get_docker_client()
        try:
            container = client.containers.get(self.container_id)
        except:
            # No such container
            pass
        return super(Instance, self).delete(*args, **kwargs)