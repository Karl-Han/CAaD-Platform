from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import reverse

from .models import UserAuxiliary

# Register your models here.
@admin.register(UserAuxiliary)
class UserAuxiliaryAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    list_display = ("get_user_link", "realname", "uid")
    # readonly_fields = ("user", )

    fieldsets = (
        ("Main information", {
            "fields": (
                'user',
            ),
        }),
        ("Extra information", {
            "fields": (
                "realname", "uid"
            )
        }),
    )
    def get_user_link(self, obj):
        return format_html('<a href="{}">{}</a>', 
            reverse("admin:auth_user_change", args=[obj.user.pk]), obj.user.username)