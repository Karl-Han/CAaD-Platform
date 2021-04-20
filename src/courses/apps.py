from django.apps import AppConfig
# from .signals import update_user_privilege_signal


class CoursesConfig(AppConfig):
    name = 'courses'

    def ready(self):
        # from .models import update_member_privilege_staff
        # update_user_privilege_signal.connect(update_member_privilege_staff)

        return super().ready()
