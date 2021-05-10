from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, reverse

from courses.models import CourseMember

# check_func(user) -> bool
@login_required
def user_pass(check_func):
    pass_test = user_passes_test(check_func)

    def decorator(view_func):
        return pass_test(view_func)

    return decorator
# 1. user_login_and_pass(check_func)
# 2. @decorator -> decorator(view_func)(*args, **kwargs)
# 3. user_passes_test(check_func)(view_func)(*args, **kwargs)

@login_required
def user_is_teacher(view_func):
    return permission_required()

class SetLoginRequiredMixin(LoginRequiredMixin):
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            messages.info(request, "Please login to continue")
            print(e)
            return redirect(reverse("login"))

class CheckGreaterPrivilegeMixin(SetLoginRequiredMixin, UserPassesTestMixin):
    least_privilege = 3

    def test_func(self):
        if self.course_id == None:
            raise Exception("course_id not set")
        else:
            print("Check {} least({}) in Course({})".format(self.request.user.pk, self.least_privilege, self.course_id))
            return (CourseMember.get_highest_course_privilege(self.request.user.pk, self.course_id) <= self.least_privilege) | self.request.user.is_superuser
        return False

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, "Permission Denied, login may help")
            print("Exception occur")
            return redirect(reverse("login"))