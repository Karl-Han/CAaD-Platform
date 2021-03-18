from django.core.exceptions import PermissionDenied
from django.views import View
from django.contrib import messages
from django.shortcuts import render

from homeworks.models import Task
from files.forms import UploadDockerfileForm
from files.models import DockerFile
from utils.params import DOCKER_BASE_URL
from .models import Image

class UploadDockerfileView(View):
    def get(self, request, task_id):
        form = UploadDockerfileForm()
        return render(request, "dockers/upload.html", {"form": form, "task_id": task_id})

    def post(self, request, task_id):
        form = UploadDockerfileForm(request.POST, request.FILES)
        task = Task.objects.get(pk=task_id)

        if form.is_valid():
            # Save dockerfile
            dockerfile = DockerFile(
                file = form.cleaned_data['file']
            )
            dockerfile.save()

            # Initialize docker image
            image = Image(
                port_open=form.cleaned_data['port_open'],
                dockerfile = dockerfile, 
                task = task
            )
            image.save()
            messages.info(request, "Successfully Upload Dockerfile zip")
        return render(request, "dockers/upload.html", {"form": form})