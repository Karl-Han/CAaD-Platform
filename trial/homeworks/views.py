from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied, ValidationError
from django.views import View
from django.views.generic import ListView, UpdateView
from django.views.generic.base import ContextMixin
from django.contrib import messages

from courses.models import Course, CourseMember
from .forms import TaskForm
from .models import Task, Submission
# HomeworkStatu is Submission now
from files.forms import UploadFileForm

import json
import datetime

from utils.general import return_error, check_authenticated_and
from utils.status import *
from .utils import SUBMISSION_STATUS

class TaskListView(ListView):
    """
    List all the tasks in the same course
    """
    paginate_by = 10
    template_name = 'homeworks/task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Task.objects.filter(course__pk=course_id)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['title'] = "Task List"
        return context

    def get(self, request, course_id):
        res, response = check_authenticated_and(request, CourseMember.is_member_of(request.user.pk, course_id), USER_NOT_AUTHORIZED)
        if res == False:
            return response

        # Authorized user
        return super(TaskListView, self).get(self, request)
    

class CreateTaskView(View, ContextMixin):
    template_name = "homeworks/task_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Task"
        return context
    
    def get(self, request, course_id):
        context = self.get_context_data()
        context['form'] = TaskForm()
        context['course_id'] = course_id
        context['is_teacher'] = (CourseMember.get_highest_course_privilege(request.user.pk, course_id) < 2)
        return render(request, self.template_name, context)
        
    def post(self, request, course_id):
        res, response = check_authenticated_and(request, CourseMember.is_teacher_of(request.user.pk, course_id), USER_NOT_AUTHORIZED)
        if res == False:
            return response

        # Authorized as teacher
        form = TaskForm(request.POST)
        if form.is_valid():
            # Submitted fields: title, description, tips, close_date, answer
            task = form.save()
            task.course = get_object_or_404(Course, pk=course_id)
            task.creator = request.user
            task.save()
            messages.info(request, "Create Task successfully")
            return redirect(reverse("courses:task_list", args=[course_id]))

        context = self.get_context_data()
        context['form'] = form
        context['course_id'] = course_id
        return render(request, self.template_name, {"form": form, 'course_id': course_id})

class TaskDetailView(View, ContextMixin):
    """
    Display the detail of specific task

    Privilege: more than student
    
    For students of the task:
        * Display details of the task
        * Upload, delete the commited file
    For non-students:
        * Display details of the task
        * Redirect to submissions of the task
    """
    template_name = "homeworks/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Task Detail"
        return context

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if request.user.is_authenticated and CourseMember.is_member_of(request.user.pk, task.course.pk):
            # User is member
            privilege = CourseMember.get_highest_course_privilege(request.user.pk, task.course.pk)
            context = self.get_context_data()
            context['task'] = task
            if privilege == 3:
                # One and only one
                try:
                    submission = Submission.objects.get(task__pk=task_id, submitter__pk=request.user.pk)
                    context['submission'] = submission
                except Submission.DoesNotExist:
                    # submission = None
                    submission = Submission(submitter=request.user, task=task)
                    submission.save()
                except Exception as e:
                    # More than one copy
                    print(e)
                    # messages.error("More than one copy for {} in {}".format(request.user.pk, task_id))
                    raise e
                finally:
                    context['submission'] = submission
                    try:
                        file = submission.file
                        print(file.name)
                    except:
                        context['to_submit'] = True
                        context['form'] = UploadFileForm()
            else:
                # link to submission list
                context["is_teacher"] = True
                context['']
            return render(request, self.template_name, context=context)
        return return_error(request, USER_NOT_AUTHENTICATED)

    def post(self, request, task_id):
        context = self.get_context_data()
        task = get_object_or_404(Task, pk=task_id)

        if request.user.is_authenticated and CourseMember.is_student_of(request.user.pk, task.course.pk):
            try:
                submission = Submission.objects.get(task__pk=task_id, submitter__pk=request.user.pk)
                form = UploadFileForm(files=request.FILES)
                if form.is_valid():
                    file = form.save()
                    submission.file = file
                    submission.save()
                    messages.info(request, "Successfully submit homework")
                    return redirect(reverse("courses:task_detail", args=[task_id]))
                messages.info(request, "Fail to validate form.")
                context['form'] = form
                print(form.errors)
                return render(request, self.template_name, context=context)
            except Submission.DoesNotExist:
                # Normal case
                form = UploadFileForm(files=request.FILES)
                if form.is_valid():
                    file = form.save()
                    submission = Submission(submitter=request.user, task=task, file=file)
                    submission.save()
                    messages.info(request, "Successfully submit homework")
                    return redirect(reverse("courses:task_detail", args=[task_id]))
                messages.info(request, "Fail to validate form.")
                context['form'] = form
                print(form.errors)
                return render(request, self.template_name, context=context)
            except Exception as e:
                # More than one copy
                print(e)
                messages.error("More than one copy for {} in {}".format(request.user.pk, task_id))
                return redirect(reverse("courses:task_detail", args=[task_id]))
        return redirect(reverse("courses:task_detail", args=[task_id]))

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
        context['title'] = "Submission List"
        context['task_id'] = self.kwargs['task_id']
        return context

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)

        res, response = check_authenticated_and(request, CourseMember.is_teacher_of(request.user.pk, task.course.pk), USER_NOT_AUTHORIZED)
        if res == False:
            return response

        # Authorized user
        return super(SubmissionListView, self).get(self, request)

class SubmissionCommentUpdateView(UpdateView):
    model = Submission
    fields = ["status", "score", "comment"]
    success_url = "/"
    template_name = "homeworks/submission_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission_id = self.object.pk
        # download_link = self.object.get_download_url()
        file_id = self.object.file.pk

        context['submission_id'] = submission_id
        context['title'] = "Comment Submission"
        # context['file_download_url'] = download_link
        context['file_id'] = file_id
        return context

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

class TaskUpdateView(UpdateView):
    model = Task
    fields = ["title", "description", "tips", "answer", "status", "close_date"]
    # To be change
    success_url = "/"
    template_name = "homeworks/task_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_id'] = self.object.pk
        context['title'] = "Task Update"

        return context

    def form_valid(self, form):
        self.success_url = reverse("courses:task_detail", args=[self.object.pk])
        return super().form_valid(form)