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
                'title', 'course', "creator", "dockerfile"
            ),
        }),
        ("Extra information", {
            "fields": (
                "status", "description", "have_docker"
            )
        }),
    )

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("pk", "submitter", "task", "file", "status")

    fieldsets = (
        ("Main information", {
            "fields": (
                'submitter', "task"
            ),
        }),
        ("Extra information", {
            "fields": (
                "file", "status"
            )
        }),
    )