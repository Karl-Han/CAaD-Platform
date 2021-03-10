from django.contrib import admin
from .models import Course, CourseMember

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("pk", "name", "password", "creator", "create_date")

    fieldsets = (
        ("Main information", {
            "fields": (
                'name', 'password', 'creator'
            ),
        }),
        ("Extra information", {
            "fields": (
                "create_date", "description"
            )
        }),
    )
    
@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("course", "user", "type")

    fieldsets = (
        ("Main information", {
            "fields": (
                'course', 'user', 'type'
            ),
        }),
    )
    