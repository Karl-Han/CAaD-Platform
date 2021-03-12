from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied, ValidationError
from django.views import View
from django.views.generic import ListView, UpdateView
from django.contrib import messages

from users.models import User
from courses.models import Course, CourseMember
from .forms import TaskForm
from .models import Task, Submission
# HomeworkStatu is Submission now
# from homeworks.models import Homework, HomeworkStatu

import json
import datetime

from utils.check import info, checkReqData, checkUser, return_error
from utils.status import *
from .utils import SUBMISSION_STATUS

class TaskListView(ListView):
    paginate_by = 10
    template_name = 'homeworks/task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Task.objects.filter(course__pk=course_id)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context

    def get(self, request, course_id):
        if not request.user.is_authenticated or not CourseMember.is_teacher_of(request.user.pk, course_id):
            return return_error(request, NOT_AUTHENTICATED)

        # Authorized user
        return super(TaskListView, self).get(self, request)

    

class CreateTaskView(View):
    def get(self, request, course_id):
        form = TaskForm()
        return render(request, "homeworks/task_create.html", {"form": form, 'course_id': course_id})
        
    def post(self, request, course_id):
        if not request.user.is_authenticated or not CourseMember.is_teacher_of(course_id, request.user.pk):
            return return_error(request, NOT_AUTHENTICATED)

        # Authorized as teacher
        form = TaskForm(request.POST)
        if form.is_valid():
            # Submitted fields: title, description, tips, close_date, answer
            task = form.save()
            task.course = get_object_or_404(Course, pk=course_id)
            task.creator = request.user
            task.save()
            messages.info(request, "Create Task successfully")
            return redirect(reverse("homeworks:task_list", args=[course_id]))
            
        return render(request, "homeworks/task_create.html", {"form": form, 'course_id': course_id})

# For student: modify submission
# For > student: read submission
class TaskDetailView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if request.user.is_authenticated and CourseMember.is_member_of(request.user.pk, task.course.pk):
            # User is member
            privilege = CourseMember.get_course_privilege(request.user.pk, task.course.pk)
            context = {}
            context['task'] = task
            if privilege == 3:
                # One and only one
                try:
                    submission = Submission.objects.get(task__pk=task_id, user__pk=request.user.pk)
                    context['submission'] = submission
                except Submission.DoesNotExist:
                    # submission = None
                    context['to_submit'] = True
                    context['task_id'] = task_id
                    context['form'] = UploadFileForm()
                    pass
                except:
                    # More than one copy
                    messages.error("More than one copy for {} in {}".format(request.user.pk, task_id))
            else:
                # link to submission list
                context["is_teacher"] = True
                context['task_id'] = task_id

            return render(request, "homeworks/task_detail.html", context=context)
        return return_error(request, NOT_AUTHENTICATED)
    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if request.user.is_authenticated and CourseMember.is_student_of(request.user.pk, task.course.pk):
            try:
                submission = Submission.objects.get(task__pk=task_id, user__pk=request.user.pk)
            except Submission.DoesNotExist:
                # Normal case
                form = UploadFileForm(request.POST, request.FILES)
                file = form.save()
                submission = Submission(course=task.course, user=request.user, task=task, file=file)
                submission.save()
            except:
                # More than one copy
                messages.error("More than one copy for {} in {}".format(request.user.pk, task_id))
                return redirect(reverse("task_detail", args=[task_id]))
        return redirect(reverse("task_detail", args=[task_id]))

class SubmissionListView(ListView):
    paginate_by = 10
    template_name = 'homeworks/submission_list.html'
    context_object_name = 'submission_list'

    def get_queryset(self):
        user = self.request.user
        task_id = self.kwargs['task_id']
        return Submission.objects.filter(task__pk=task_id)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['task_id'] = self.kwargs['task_id']
        return context

    def get(self, request, task_id):
        task = get_object_or_404(Task, task_id)
        if not request.user.is_authenticated or not CourseMember.is_teacher_of(request.user.pk, task.course.pk):
            return return_error(request, NOT_AUTHENTICATED)

        # Authorized user
        return super(SubmissionListView, self).get(self, request)

class SubmissionCommentUpdateView(UpdateView):
    model = Submission
    fields = ["status", "score", "comment"]
    success_url = "/"
    template_name = "submission_update.html"

    def clean_score(self):
        score = self.cleaned_data['score']
        if score > 100 or score < 0:
            raise ValidationError("Invalid score for submission")
        return score

    def form_valid(self, form):
        self.success_url = reverse("submission_list", args=[self.object.task.pk])
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return super(SubmissionCommentUpdateView, self).get(self, request, *args, **kwargs)