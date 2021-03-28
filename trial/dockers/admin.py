from django.contrib import admin
from .models import Image, Instance

# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("pk", "image_id", "port_open", "dockerfile", "task")

    fieldsets = (
        ("Main information", {
            "fields": (
                'image_id', "port_open"
            ),
        }),
        ("Extra information", {
            "fields": (
                "dockerfile", "task"
            )
        }),
    )

@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("pk", "part_of_id", "port_local",
         "port_server", "submission", "create_date")

    fieldsets = (
        ("Main information", {
            "fields": (
                'container_id', "port_local", "port_server"
            ),
        }),
        ("Extra information", {
            "fields": (
                "submission", "create_date", "update_date"
            )
        }),
    )
    def part_of_id(self):
        return self.container_id[:5]