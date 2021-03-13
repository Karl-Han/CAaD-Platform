from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


from courses.models import Course
from files.models import SubmissionFile

# Create your models here.


class Task(models.Model):
    TASK_STATUS = [(0, 'draft'), (1, 'running'), (2, 'closed')]

    # main info
    title = models.CharField('title', max_length=64)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tasks", null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_created", null=True)
    description = models.CharField('description', max_length=1024)
    tips = models.CharField('tips', max_length=1024, blank=True)
    answer = models.CharField('answer', max_length=1024, blank=True)
    dockerAPI = models.CharField('dockerAPI', max_length=128, blank=True)

    # status info
    status = models.IntegerField(
        'homework status', choices=TASK_STATUS, default=0)
    create_date = models.DateTimeField('date created', default=timezone.now())
    close_date = models.DateTimeField(
        'date to close', default=timezone.now() + timedelta(days=30))


class Submission(models.Model):
    SUBMISSION_STATUS = [ (0, "Unfinished"), (1, "Submitted"), (2, "Commented") ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="submissions", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions", null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="submissions", null=True)
    file = models.OneToOneField(SubmissionFile, on_delete=models.CASCADE, null=True, related_name="submission")

    status = models.IntegerField(
        'status', default=0, choices=SUBMISSION_STATUS)
    commit_date = models.DateTimeField('date committed', default=timezone.now())
    # types = ( (0, 'uncomment'), (1, 'commented') )
    # types = models.IntegerField('homework types')
    # answer = models.CharField('answer', max_length=1024)
    score = models.IntegerField('score', blank=True)
    comment = models.CharField('comment', max_length=1024, blank=True)

    def get_file_path(self):
        return "#"
