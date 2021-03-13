from django.contrib import admin

from .models import SubmissionFile

# Register your models here.
@admin.register(SubmissionFile)
class SubmissionFileAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("pk", "file_name", "file", "create_date", "file_hash")

    fieldsets = (
        ("Main information", {
            "fields": (
                'file_name', 'file'
            ),
        }),
        ("Extra information", {
            "fields": (
                "create_date", "file_hash"
            )
        }),
    )