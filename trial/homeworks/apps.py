from django.apps import AppConfig


class HomeworksConfig(AppConfig):
    name = 'homeworks'

    def ready(self):
        from .signals import updateHwStatus
