from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import reverse

from .models import Course, CourseMember
from homeworks.models import Task

class CourseCreatorFilter(admin.SimpleListFilter):
    """
    Customized filter for visible courses
    """
    title = "Creator"
    parameter_name = 'creator_id'

    def lookups(self, request, model_admin):
        user = request.user

        if user.is_superuser:
            queryset_valid = Course.objects.filter()
        else:
            teacher_list = Course.get_all_teacher_courses(user)
            queryset_valid = Course.objects.filter(pk__in=teacher_list)

        res = set([(c.creator.pk, c.creator.username) for c in queryset_valid])
        return res

    def queryset(self, request, queryset):
        creator_id = self.value()
        if creator_id:
            return queryset.filter(creator=creator_id)
        return queryset


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True

    list_display = ("course_link", "password", "creator_link", "create_date", "task_count")
    list_filter = [CourseCreatorFilter, ]

    search_fields = ["name"]

    fieldsets = (
        ("Main information", {
            "fields": (
                'name', 'password'
            ),
        }),
        ("Extra information", {
            "fields": (
                "create_date", "description"
            )
        }),
    )

    def get_queryset(self, request):
        queryset = super(CourseAdmin, self).get_queryset(request)
        user = request.user

        if not user.is_superuser:
            teacher_list = Course.get_all_teacher_courses(user)
            queryset = queryset.filter(pk__in=teacher_list)

        return queryset

    def course_link(self, obj):
        return format_html('<a href="{}">{}</a>', 
            reverse("admin:courses_course_change", args=[obj.pk]), obj.name
        )
    course_link.short_description = "Course"

    def creator_link(self, obj):
        return format_html('<a href="{}">{}</a>', 
            reverse("users:profile", args=[obj.creator.username]), obj.creator.username
        )
    creator_link.short_description = "Creator"

    def task_count(self, obj):
        return format_html('<a href="{}?course__id={}">{}</a>', 
            reverse("admin:homeworks_task_changelist"), obj.pk, Task.objects.filter(course=obj).count()
        )
    task_count.short_description = "Tasks"
    
@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("course", "user", "type")
    readonly_fields = ("course", "user", )

    fieldsets = (
        ("Main information", {
            "fields": (
                'course', 'user', 'type'
            ),
        }),
    )
    
    def get_queryset(self, request):
        queryset = super(CourseMemberAdmin, self).get_queryset(request)
        user = request.user

        if user.is_superuser:
            return queryset

        course_as_teacher_list = Course.get_all_teacher_courses(user)
        return queryset.filter(course__pk__in=course_as_teacher_list)