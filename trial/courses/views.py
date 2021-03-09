from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.views.generic import View, ListView, DetailView, UpdateView
from Crypto.Hash import SHA3_256
from datetime import datetime

from users.models import User
from .models import Course, CourseMember
from homeworks.models import Homework, HomeworkStatu
from .forms import CreateCourseForm # , EditCourseForm
import courses.utils as utils

import json
import random

from utils.check import info, Visitor, checkTokenTimeoutOrLogout, checkUserLoginOrVisitor, checkReqData, checkUser
from utils.status import *
from .utils import getRandCPwd, getCM, getHw

class IndexListView(ListView):
    queryset = Course.objects.order_by('name').all()
    paginate_by = 2
    context_object_name = "course_list"
    template_name = "courses/index.html"

class CreatecourseView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "courses/info.html", {"info": "User not authenticated."})
        form = CreateCourseForm(creator=request.user)
        return render(request, 'courses/create.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return render(request, "courses/info.html", {"info": "User not authenticated."})
        # Create a course for him
        user = request.user
        form = CreateCourseForm(request.POST, creator=user)
        if not form.is_valid():
            return render(request, 'courses/info.html', {"info": "Successfully create course"})

        print(form.cleaned_data)
        # form.cleaned_data['creator'] = user
        obj = form.save()
        obj.creator = user
        obj.save()

        # Add role in CourseMember
        cm = CourseMember(
            course = obj, 
            user = user,
            type = utils.COURSEMEMBER_ADMIN
        )
        cm.save()

        # Set user as staff
        user.is_staff = True
        user.save()

        return render(request, 'courses/info.html', {"info": "Successfully create course"})

def coursePage(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {}
    user = request.user

    # Two stages
    # 1. Open to everyone or member -> basic info
    # 2. Is teacher -> to member management
    # Stage 1
    privilege = CourseMember.get_course_privilege(user.pk, course.pk)
    print(privilege)
    if course.is_open or privilege != -1:
        context['course'] = course
        if privilege == -1:
            context['role'] = "Visitor"
        else:
            context['role'] = utils.COURSEMEMBER_TYPE[privilege]
    
    # Stage 2
    if CourseMember.is_teacher_of(user.pk, course_id):
        context['is_teacher'] = True
    
    return render(request, "courses/homepage.html", context=context)

class EditcourseView(UpdateView):
    model = Course
    fields = ['name', 'password', 'description', 'is_open']
    success_url = "/"

    def form_valid(self, form):
        clean = form.cleaned_data
        if clean['password'] == '':
            self.object.password = getRandCPwd()
            self.object.save()
        self.success_url = reverse("courses:homepage", args=[self.object.pk])
        return super().form_valid(form)

def joinCourse(request, course_id):
    pass