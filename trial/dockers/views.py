from django.core.exceptions import PermissionDenied
from django.views import View
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, reverse, redirect

from homeworks.models import Task
from files.forms import UploadDockerfileForm
from files.models import DockerFile
from utils.params import DOCKER_BASE_URL
from .models import Image
from utils.general import error_not_authenticated, return_error, info
from homeworks.models import Submission

class UploadDockerfileView(View):
    template_name = "dockers/dockerfile_upload.html"

    def get(self, request, task_id):
        form = UploadDockerfileForm()
        return render(request, self.template_name, {"form": form, "task_id": task_id})

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
            image.task.have_docker = True
            image.task.save()
            messages.info(request, "Successfully Upload Dockerfile zip")
        return render(request, self.template_name, {"form": form})

def containerStatus(request, submission_id):
    # Render status of container in submission for user
    context = {}
    context["submission_id"] = submission_id
    user = request.user

    if not user.is_authenticated:
        return error_not_authenticated(request)
    
    submission = get_object_or_404(Submission, pk=submission_id)
    try:
        instance = submission.instance
        context['status'] = 1
        context['instance'] = instance
    except:
        context['status'] = 0
        print("Not exist")
        pass

    return render(request, "dockers/container.html", context)

def createContainer(request, submission_id):
    # Create container for specific user in submission
    submission = get_object_or_404(Submission, pk=submission_id)
    task = submission.task
    if task.have_docker:
        image = task.image
        container_id, port_server = image.run_new_container(submission_id)
        print("container({}): port({})".format(container_id, port_server))
    else:
        return info(request, "No dockerfile for task({})".format(task.pk), reverse("dockers:containerStatus", args=[submission_id]))

    return redirect(reverse("dockers:container_status", args=[submission_id]))

def deleteContainer(request, submission_id):
    # Delete container for specific user in submission
    submission = get_object_or_404(Submission, pk=submission_id)
    instance = None

    try:
        instance = submission.instance
        instance.delete()
    except:
        return info(request, "No instance for submission({})".format(submission.pk), reverse("dockers:containerStatus", args=[submission_id]))

    return redirect(reverse("dockers:container_status", args=[submission_id]))
