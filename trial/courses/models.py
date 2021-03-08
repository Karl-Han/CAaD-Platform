from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

root = User.objects.get(username="root")

class Course(models.Model):
    # COURSE_STATUS = [(0, 'to be activate'), (1, 'unstarted'),
    #                  (2, 'running'), (3, 'closed')]

    # main info
    name = models.CharField('course name', max_length=32)
    # digits and upper char (generate randomly)
    password = models.CharField('joining password', max_length=8)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    # status info
    # status = models.IntegerField(
    #     choices=COURSE_STATUS, verbose_name='course status')
    # types = models.IntegerField('course types')  # reserved
    create_date = models.DateTimeField('date created up', default=now())
    description = models.CharField('description', max_length=512)
    # popularity = models.IntegerField('popularity')  # for recommending
    is_open = models.BooleanField("Is open to all", default=True)

    def __str__(self):
        return "Course({}-{})".format(self.name, self.creator.username)

class CourseMember(models.Model):
    MEMBER_TYPE = [(0, 'admin'), (1, 'teacher'),
                   (2, 'asistant'), (3, 'student')]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type = models.IntegerField(
        choices=MEMBER_TYPE, verbose_name='Member type')