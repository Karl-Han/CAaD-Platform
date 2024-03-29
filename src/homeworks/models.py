from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.http import FileResponse

from courses.models import Course
from files.models import SubmissionFile, DockerFile

class Task(models.Model):
    TASK_STATUS = [(0, 'draft'), (1, 'running'), (2, 'closed')]

    # main info
    title = models.CharField('title', max_length=64)
    description = models.CharField('description', max_length=1024)
    tips = models.CharField('tips', max_length=1024, blank=True)
    answer = models.CharField('answer', max_length=1024, blank=True)
    have_docker = models.BooleanField("have docker experiment", default=False)
    dockerfile = models.OneToOneField(DockerFile, on_delete=models.SET_NULL, blank=True, null=True)
    auxiliary_file = models.OneToOneField(SubmissionFile, on_delete=models.SET_NULL, blank=True, null=True)

    # status info
    status = models.IntegerField(
        'homework status', choices=TASK_STATUS, default=0)
    create_date = models.DateTimeField('date created', default=timezone.now())
    close_date = models.DateTimeField(
        'date to close', default=timezone.now() + timedelta(days=30))

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tasks", null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_created", null=True)

    def __str__(self):
        return "Task({}):{}".format(self.pk, self.title)


class Submission(models.Model):
    SUBMISSION_STATUS = [ (0, "Unfinished"), (1, "Submitted"), (2, "Commented") ]

    status = models.IntegerField(
        'status', default=0, choices=SUBMISSION_STATUS)

    commit_date = models.DateTimeField('date committed', default=timezone.now())
    score = models.IntegerField('score', null=True)
    comment = models.CharField('comment', max_length=1024, null=True)

    # course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="submissions", null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="submissions", null=True)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions", null=True)
    file = models.OneToOneField(SubmissionFile, on_delete=models.SET_NULL, null=True, blank=True, related_name="submission")

    def get_file_response(self):
        path = self.file.get_local_path()
        response = FileResponse(open(path, "rb"), filename=self.file.name)
        print(path)
        return response
