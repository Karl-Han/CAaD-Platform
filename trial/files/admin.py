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
    list_display = ("pk", "name", "file", "create_date", "hash", "status")

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
        # return super().save_model(request, obj, form, change)