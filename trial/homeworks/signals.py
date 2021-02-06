from django.db.models.signals import post_init
from django.dispatch import receiver

from homeworks.models import Homework

from django.utils import timezone
import datetime

@receiver(post_init, sender=Homework)
def updateHwStatus(instance=None, **kwargs):
    cl = instance.close_date
    if cl-timezone.now() < datetime.timedelta(seconds=0):
        instance.status = 2
