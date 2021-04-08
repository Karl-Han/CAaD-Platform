from django.views.generic import View, ListView, DetailView, UpdateView

from homeworks.models import Task
from .models import Course, CourseMember

class MyTeachingCourseListView(ListView):
    paginate_by = 3
    context_object_name = "course_list"
    template_name = "courses/index.html"

    def get_queryset(self):
        queryset = Course.objects.all()
        teacher_list = Course.get_all_teacher_courses(self.request.user)
        return queryset.filter(pk__in=teacher_list).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Teaching Courses"
        return context

class MyStudyingCourseListView(ListView):
    paginate_by = 3
    context_object_name = "course_list"
    template_name = "courses/index.html"

    def get_queryset(self):
        queryset = Course.objects.all()
        student_list = Course.get_all_student_courses(self.request.user)
        return queryset.filter(pk__in=student_list).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Studying Courses"
        return context

class MyTasksListView(ListView):
    paginate_by = 10
    template_name = 'courses/tasks.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        user = self.request.user
        student_list = Course.get_all_student_courses(self.request.user)
        return Task.objects.filter(course__pk__in=student_list)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['title'] = "Task List"
        return context