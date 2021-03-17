from django.contrib import admin
from .models import Course, CourseMember

class CourseCreatorFilter(admin.SimpleListFilter):
    """
    Customized filter for visible courses
    """
    title = "Filter"
    parameter_name = 'course_creator'

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
        creator = self.value()
        if creator:
            return queryset.filter(creator=creator)
        return queryset


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("pk", "name", "password", "creator", "create_date")
    list_filter = [CourseCreatorFilter, ]

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

        if user.is_superuser:
            return queryset

        teacher_list = Course.get_all_teacher_courses(user)
        return queryset.filter(pk__in=teacher_list)
    
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