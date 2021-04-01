from django.contrib import admin

class MyAdminSite(admin.AdminSite):
    site_header = "CAaD platform administration"
    site_title = "CAaD site admin"