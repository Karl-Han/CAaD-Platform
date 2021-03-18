from django.contrib import admin

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