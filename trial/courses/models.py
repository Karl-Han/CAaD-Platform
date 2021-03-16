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

    @classmethod
    def is_password_for_course(cls, course_id, pwd_to_check):
        obj = cls.objects.get(pk=course_id)
        if obj:
            return (obj.password == pwd_to_check)
        return False


class CourseMember(models.Model):
    MEMBER_TYPE = [(0, 'admin'), (1, 'teacher'),
                   (2, 'asistant'), (3, 'student')]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type = models.IntegerField(
        choices=MEMBER_TYPE, verbose_name='Member type')
    
    @classmethod
    def get_highest_course_privilege(cls, user_id, course_id):
        if user_id == None or course_id == None:
            return 4

        cm = cls.objects.filter(course__pk=course_id).filter(user__pk=user_id)

        if len(cm) > 0:
            # Probably multiple role, pick the highest privilege
            type = 3
            for role in cm:
                if role.type < type:
                    type = role.type
            return type
        return 4

    @classmethod
    def is_teacher_of(cls, user_id, course_id):
        """
        Check user is teacher of course

        Input:
            * user_id: user's id
            * course_id: courses's id
        Output:
            * True/False
        """
        return (cls.get_highest_course_privilege(user_id, course_id) < 2)

    @classmethod
    def is_student_of(cls, user_id, course_id):
        cm = cls.objects.filter(course__pk=course_id).filter(user__pk=user_id)

        for role in cm:
            if role.type == 3:
                return True
        return False

    @classmethod
    def is_member_of(cls, user_id, course_id):
        return (cls.get_highest_course_privilege(user_id, course_id) < 4)
    
    @classmethod
    def join_course_as_student(cls, user_id, course_id):
        course = Course.objects.get(pk=course_id)
        user = User.objects.get(pk=user_id)
        cm = cls(course=course, user=user, type=3)
        cm.save()

    @classmethod
    def update_member_privilege_staff(cls, user_id):
        user = User.objects.get(pk=user_id)
        cms = CourseMember.objects.filter(user__pk=user_id)
        type = 4
        for cm in cms:
            if cm.type < type:
                type = cm.type
        if type > 2:
            user.is_staff = False
        else:
            user.is_staff = True
        user.save()