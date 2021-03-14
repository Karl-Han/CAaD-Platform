from django.contrib import admin

from .models import Task, Submission
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("pk", "title", "description", "course", "creator", "status")

    fieldsets = (
        ("Main information", {
            "fields": (
                'title', 'course', "creator"
            ),
        }),
        ("Extra information", {
            "fields": (
                "status", "description"
            )
        }),
    )

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("pk", "course", "user", "task", "file", "status")

    fieldsets = (
        ("Main information", {
            "fields": (
                'course', 'user', "task"
            ),
        }),
        ("Extra information", {
            "fields": (
                "file", "status"
            )
        }),
    )