from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, UpdateView
from django.views.generic.base import ContextMixin
from django.contrib import messages

from users.models import User
from utils.general import error_not_authenticated, return_error, info
from .models import Course, CourseMember
from .forms import CreateCourseForm, JoinForm
from courses.utils import *

from .utils import getRandCPwd
# from .signals import update_user_privilege_signal

class IndexListView(ListView):
    queryset = Course.objects.order_by('name').all()
    paginate_by = 3
    context_object_name = "course_list"
    template_name = "courses/index.html"

class CreatecourseView(View, ContextMixin):
    template_name = 'courses/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Course"
        return context
    

    def get(self, request):
        if not request.user.is_authenticated:
            return error_not_authenticated(request)

        context = self.get_context_data()
        form = CreateCourseForm(creator=request.user)
        context['form'] = form

        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            error_not_authenticated(request)

        # Create a course for him
        user = request.user
        form = CreateCourseForm(request.POST, creator=user)
        if form.is_valid():
            # Save creator
            obj = form.save()
            obj.creator = user
            obj.save()
            # Add role in CourseMember
            cm = CourseMember(
                course = obj, 
                user = user,
                type = COURSEMEMBER_ADMIN
            )
            cm.save()
            # Set user as staff
            user.is_staff = True
            user.save()

            return info(request, "Successfully create course", redirect_to=reverse("courses:course_homepage", args=[obj.pk]))
        return return_error(request, FORM_NOT_VALID)

def homepage(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    context = {}
    context['title'] = "Course Homepage"

    # Two stages
    # 1. Open to everyone or member -> basic info
    # 2. Is teacher -> to member management
    # Stage 1
    privilege = CourseMember.get_highest_course_privilege(user.pk, course.pk)
    if course.is_open or privilege != 4:
        context['course'] = course

        if privilege == 4:
            context['role'] = "Visitor"
            form = JoinForm(initial={"id": course_id})
            context['join_form'] = form
        else:
            context['role'] = COURSEMEMBER_TYPE[privilege]
            context['is_member'] = True
    
    # Stage 2
    if CourseMember.is_teacher_of(user.pk, course_id):
        context['is_teacher'] = True
    
    return render(request, "courses/homepage.html", context=context)

class EditcourseView(UpdateView):
    model = Course
    fields = ['name', 'password', 'description', 'is_open']
    success_url = "/"
    template_name = "courses/update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] =  "Edit Course"
        return context

    def form_valid(self, form):
        clean = form.cleaned_data
        if clean['password'] == '':
            self.object.password = getRandCPwd()
            self.object.save()
        self.success_url = reverse("courses:course_homepage", args=[self.object.pk])
        return super().form_valid(form)

def joinCourse(request, course_id):
    if request.method != "POST":
        return info(request, "Wrong HTTP method for {}. POST only".format(request.path),
                redirect_to=reverse("courses:course_homepage", args=[course_id]))

    if not request.user.is_authenticated:
        return error_not_authenticated(request)

    # Check password and join class
    form = JoinForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        if Course.is_password_for_course(course_id, data['password']):
            CourseMember.join_course_as_student(request.user.pk, course_id)
            return info(request, "Successfully join as student.", reverse("courses:course_homepage", args=[course_id]))
    return return_error(request, FORM_NOT_VALID)

class StudentsListView(ListView):
    paginate_by = 10
    template_name = 'courses/students.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        user = self.request.user
        course_id = self.kwargs['course_id']
        privilege = CourseMember.get_highest_course_privilege(user.pk, course_id)
        return CourseMember.objects.filter(course__id=course_id, type__gt=privilege)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['title'] = "Student List"
        context['course_id'] = self.kwargs['course_id']
        return context

    def get(self, request, course_id):
        if not request.user.is_authenticated:
            return error_not_authenticated(request)

        if not CourseMember.is_teacher_of(request.user.pk, course_id):
            return return_error(USER_NOT_AUTHORIZED)

        # Authorized user
        # self.object_list = self.object_list.filter(type__lt=CourseMember.get_course_privilege(request.user.pk, course_id))
        return super(StudentsListView, self).get(self, request)

class ChangePrivilegeView(View, ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Change Member Privilege"
        return context
    

    def get(self, request, member_record):
        course = get_object_or_404(CourseMember, pk=member_record).course
        if not CourseMember.is_teacher_of(request.user.pk, course.pk):
            return return_error(USER_NOT_AUTHORIZED)

        cm = get_object_or_404(CourseMember, pk=member_record)
        context = self.get_context_data()
        context['user_local'] = cm.user
        context['type'] = cm.type
        context['type_readable'] = COURSEMEMBER_TYPE[cm.type]
        context['course_id'] = course.pk
        context['member_record'] = member_record 
        context['privilege'] = CourseMember.get_highest_course_privilege(request.user.pk, course.pk)
        return render(request, "courses/student_detail.html", context)

    def post(self, request, member_record):
        course = get_object_or_404(CourseMember, pk=member_record).course
        if CourseMember.is_teacher_of(request.user.pk, course.pk):
            cm = get_object_or_404(CourseMember, pk=member_record)
            if cm.user.pk != int(request.POST['user_id']):
                # return render(request, "courses/info.html", {"info": "Conflicting record and user."})
                return info(request, "Conflicting record and user")
            cm.type = request.POST['privilege']

            cm.save()
            return redirect(reverse("courses:students_manage", args=[course.pk]))
        return return_error(USER_NOT_AUTHORIZED)