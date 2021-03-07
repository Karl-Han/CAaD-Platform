from django.contrib import admin

# from .models import User

# Register your models here.


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     # id is the auto increment default unique value of User
#     list_display = ("id", "nickname", "email", "signup_date", "status")
#     list_filter = ("id", "nickname", "email", "signup_date", "status")
#     search_fields = ("nickname", "email")
# 
#     # Set fieldsets to control the layout of admin “add” and “change” pages.
#     # see http://127.0.0.1:8000/admin/users/user/add/
#     # that the user name and the email is in the same division
#     fieldsets = (
#         (None, {
#             "fields": (
#                 ("nickname", "email"), "signup_date", "status"
#             )
#         }),
#     )
# 