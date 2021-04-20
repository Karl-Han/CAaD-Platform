from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import reverse

from .models import SubmissionFile, DockerFile

# Register your models here.
@admin.register(SubmissionFile)
class SubmissionFileAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("pk", "name", "file", "create_date", "hash")

    fieldsets = (
        ("Main information", {
            "fields": (
                'name', 'file'
            ),
        }),
        ("Extra information", {
            "fields": (
                "create_date", "hash"
            )
        }),
    )

@admin.register(DockerFile)
class DockerFileAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("pk", "name", "file", "create_date", "hash", "status", "get_task_link")

    fieldsets = (
        ("Main information", {
            "fields": (
                "name", "file", "status"
            ),
        }),
        ("Extra information", {
            "fields": (
                "create_date", "hash"
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        update_fields = []
        if change:
            if form.initial['status'] != form.cleaned_data['status']:
                update_fields.append("status")
        
        obj.save(update_fields=update_fields)

    def get_task_link(self, obj):
        link = reverse("admin:homeworks_task_change", args=[obj.task.pk])
        return format_html("<a href='{}'>{}</a>", link, obj.task.pk)

    get_task_link.short_description = "Task"