from django.apps import AppConfig


class HomeworksConfig(AppConfig):
    name = 'homeworks'

    def ready(self):
        pass
        # from .signals import updateHwStatus
