import random
from users.models import User
from courses.models import CourseMember
from homeworks.models import Homework

def getRandCPwd(dic='1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=8):
    return ''.join(random.sample(dic, length))

def getCM(cid):
    cmem = CourseMember.objects.filter(cid=cid)
    cm = []
    for c in cmem:
        uname = User.objects.get(pk=c.uid).nickname
        cm.append({
            'uname': uname,
            'uprivilege': c.types
        })
    return cm

def getHw(cid):
    homeworks = Homework.objects.filter(cid=cid)
    hw = []
    for h in homeworks:
        ctrname = User.objects.get(pk=h.ctrid).nickname
        ans = 'Display after closed!'
        if h.status == 2:
            ans = h.answer
        hw.append({
            'id': h.pk,
            'ctrname': ctrname,
            'title': h.title,
            'description': h.description,
            'tips': h.tips,
            'answer': ans,
            'status': h.status
            # TODO: not all necessary
            # types?
        })
    return hw


