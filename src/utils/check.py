from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

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