from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, UpdateView

from users.models import User
from .models import Course, CourseMember
from homeworks.models import Homework, HomeworkStatu
from .forms import CreateCourseForm, JoinForm
from courses.utils import *

from .utils import getRandCPwd

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
            type = COURSEMEMBER_ADMIN
        )
        cm.save()

        # Set user as staff
        user.is_staff = True
        user.save()

        return render(request, 'courses/info.html', {"info": "Successfully create course"})

def homepage(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {}
    user = request.user

    # Two stages
    # 1. Open to everyone or member -> basic info
    # 2. Is teacher -> to member management
    # Stage 1
    privilege = CourseMember.get_course_privilege(user.pk, course.pk)
    print(privilege)
    if course.is_open or privilege != 4:
        context['course'] = course
        if privilege == 4:
            context['role'] = "Visitor"
            form = JoinForm()
            context['join_form'] = form
        else:
            context['role'] = COURSEMEMBER_TYPE[privilege]
            context['is_member'] = True
    
    # Stage 2
    if CourseMember.is_teacher_of(user.pk, course_id):
        context['is_teacher'] = True
    
    print(context)
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
    if request.method != "POST":
        return redirect(reverse("courses:homepage", args=[course_id]))

    if not request.user.is_authenticated:
        return render(request, "info.html", {"info": "Not authenticated yet."})

    # Check password and join class
    form = JoinForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        if Course.is_password_for_course(course_id, data['password']):
            CourseMember.join_course_as_student(course_id, request.user.pk)
            return render(request, "info.html", {"info": "Successfully join as student."})
    return render(request, "info.html", {"info": "Error occur in joining"})

class StudentsListView(ListView):
    paginate_by = 10
    template_name = 'courses/students.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        user = self.request.user
        course_id = self.kwargs['course_id']
        privilege = CourseMember.get_course_privilege(user.pk, course_id)
        return CourseMember.objects.filter(course__id=course_id, type__gt=privilege)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['course_id'] = self.kwargs['course_id']

        return context

    def get(self, request, course_id):
        if not request.user.is_authenticated or CourseMember.get_course_privilege(request.user.pk, course_id):
            return render(request, "courses/info.html", {"info": "User not authenticated."})

        # Authorized user
        # self.object_list = self.object_list.filter(type__lt=CourseMember.get_course_privilege(request.user.pk, course_id))
        return super(StudentsListView, self).get(self, request)

class ChangePrivilegeView(View):
    def get(self, request, member_record):
        course = get_object_or_404(CourseMember, pk=member_record).course
        if not CourseMember.is_teacher_of(request.user.pk, course.pk):
            return render(request, "courses/info.html", {"info": "User not authenticated."})

        cm = get_object_or_404(CourseMember, pk=member_record)
        context = {}
        context['user_local'] = cm.user
        context['type'] = cm.type
        context['type_readable'] = COURSEMEMBER_TYPE[cm.type]
        context['course_id'] = course.pk
        context['member_record'] = member_record 
        context['privilege'] = CourseMember.get_course_privilege(request.user.pk, course.pk)
        return render(request, "courses/student_detail.html", context)

    def post(self, request, member_record):
        course = get_object_or_404(CourseMember, pk=member_record).course
        if CourseMember.is_teacher_of(request.user.pk, course.pk):
            cm = get_object_or_404(CourseMember, pk=member_record)
            print(cm.user.pk)
            print(request.POST['user_id'])
            if cm.user.pk != int(request.POST['user_id']):
                return render(request, "courses/info.html", {"info": "Conflicting record and user."})
            cm.type = request.POST['privilege']
            CourseMember.update_member_privilege_staff(cm.user.pk)
            cm.save()
            return redirect(reverse("courses:manage_students", args=[course.pk]))
        return render(request, "courses/info.html", {"info": "User not authenticated."})