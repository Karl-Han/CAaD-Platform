import random
# from homeworks.models import Homework

COURSEMEMBER_TYPE = ['admin', 'teacher', 'asistant', 'student']
COURSEMEMBER_ADMIN = 0
COURSEMEMBER_TEACHER = 1
COURSEMEMBER_ASSISTANT = 2
COURSEMEMBER_STUDENT = 3


def getRandCPwd(dic='1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=8):
    return ''.join(random.sample(dic, length))