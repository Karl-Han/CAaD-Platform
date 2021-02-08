from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from users.models import User
from courses.models import Course, CourseMember
from homeworks.models import Homework, HomeworkStatu

import json
import datetime

from utils.check import info, checkReqData, checkUser
from utils.status import *
from .utils import getHs, getFh

# Create your views here.
def index(request):
    return HttpResponse("test")

def doCreate(request):
    if request.method != 'POST':
        raise PermissionDenied

    crd_st, rd = checkReqData(request, post=['cname', 'title', 'description', 'tips', 'answer', 'runsec'])  # TODO: docker
    if crd_st == -1:
        return rd
    # check delta (>0)
    if int(request.POST['runsec']) <= 0:
        return info(request, INFO_HACKER)

    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    creator = tmp

    # check course
    c = Course.objects.filter(name=request.POST['cname'])
    if not c.exists():
        return info(request, INFO_NOT_EXIST, INFO_STR[INFO_NOT_EXIST]%'[Hacker?] Course')
    c = c[0]

    # check privilege
    try:
        cm = CourseMember.objects.get(uid=creator.pk, cid=c.pk)
    except:
        return info(request, INFO_HACKER)
    if cm.types >= 3:  # student
        raise PermissionDenied

    # check same homework ?
    homework = Homework.objects.filter(cid=c.pk)
    for h in homework:
        if h.title == request.POST['title']:
            return info(request, INFO_SAME, INFO_STR[INFO_SAME]%('Homework', 'name in this course'))

    # create
    data = {
        'title': request.POST['title'],
        'description': request.POST['description'],
        'cid': c.pk,
        'ctrid': creator.pk,
        'tips': request.POST['tips'],
        'answer': request.POST['answer'],
        'dockerAPI': 'TODO',
        'status': 1,
        'types': 0,  # TODO
        'create_date': timezone.now(),
        'close_date': timezone.now()+datetime.timedelta(seconds=int(request.POST['runsec']))
    }
    #return render(request, 'info.html', {'info': json.dumps(data, indent=4, sort_keys=True, default=str)})  # debug

    try:
        h = Homework(
            title = data['title'],
            description = data['description'],
            cid = data['cid'],
            ctrid = data['ctrid'],
            tips = data['tips'],
            answer = data['answer'],
            dockerAPI = data['dockerAPI'],
            status = data['status'],
            types = data['types'],
            create_date = data['create_date'],
            close_date = data['close_date']
        )
        h.save()
    except:
        return info(request, INFO_DB_ERR)

    return info(request, SUCCESS)

def getHomework(request, hid):
    # get h u c cm
    h = get_object_or_404(Homework, pk=hid)
    try:
        c = Course.objects.get(pk=h.cid)
        ctr = User.objects.get(pk=h.ctrid)
    except:
        return info(request, INFO_DB_ERR)

    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp

    # check privilege
    try:
        cm = CourseMember.objects.get(cid=c.pk, uid=user.pk)
    except:
        raise PermissionDenied

    ans = 'Display after closed!'
    if h.status == 2:
        ans = h.answer
    hw = {
        'id': h.pk,
        'title': h.title,
        'description': h.description,
        'cname': c.name,
        'ctrname': ctr.nickname,
        'tips': h.tips,
        'answer': ans,
        'dockerAPI': 'TODO',
        'status': h.status,
        'types': 'TODO',
        'cr_date': str(h.create_date),
        'cl_date': str(h.close_date)
    }

    try:
        hs = getHs(h.pk)
        fh = getFh(h.pk)
    except:
        return info(request, INFO_DB_ERR)

    data = {
        'hw': hw,
        'hSt': hs,
        'fhs': fh
    }

    # return
    if request.method == 'GET':
        if cm.types<3:
            return render(request, 'homework/homeworkM.html', data)
        else:
            hs = HomeworkStatu.objects.filter(uid=user.pk)
            if hs.exists():
                hs = hs[0]  # only one
                data['hs'] = {
                    'answer': hs.answer,
                    'types': hs.types,
                    'score': hs.score,
                    'comment': hs.comment,
                    'status': hs.status
                }
            return render(request, 'homework/homeworkS.html', data)
    elif request.method == 'POST':
        # TODO: check M/S?
        return info(request, 0, 'TODO')
        return render(request, 'info.html', {'info': json.dumps(data)})
    else:
        raise PermissionDenied

def commitHomework(request, hid):
    if request.method != 'POST':
        raise PermissionDenied

    crd_st, rd = checkReqData(request, post=['answer'])
    if crd_st == -1:
        return rd

    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp

    # check homework and course
    h = Homework.objects.filter(pk=hid)
    if not h.exists():
        return info(request, INFO_NOT_EXIST, INFO_STR[INFO_NOT_EXIST]%'[Hacker?] Homework')
    h = h[0]

    try:
        c = Course.objects.get(pk=h.cid)
    except:
        return info(request, INFO_DB_ERR)

    # check privilege
    try:
        cm = CourseMember.objects.get(uid=user.pk, cid=c.pk)
    except:
        return info(request, INFO_DB_ERR)
    if cm.types != 3:  # not student?
        return info(request, INFO_HACKER)

    # check committed
    hs = HomeworkStatu.objects.filter(cid=c.pk, uid=user.pk, hid=h.pk)
    if hs.exists():
        hs = hs[0]
        hs.answer = request.POST['answer']
        hs.status = 2*h.status
        try:
            hs.save()
        except:
            return info(request, INFO_HACKER)
    else:
        data = {
            'cid': c.pk,
            'uid': user.pk,
            'hid': h.pk,
            'types': 0,
            'answer': request.POST['answer'],
            'score': -1,  # default
            'comment': '',  # default
            'status': 2*h.status,
            'commit_date': timezone.now()
        }
        #return render(request, 'info.html', {'info': json.dumps(data, indent=4, sort_keys=True, default=str)})  # debug

        try:
            hs = HomeworkStatu(
                cid = data['cid'],
                uid = data['uid'],
                hid = data['hid'],
                types = data['types'],
                answer = data['answer'],
                score = data['score'],
                comment = data['comment'],
                status = data['status'],
                commit_date = data['commit_date']
            )
            hs.save()
        except:
            return info(request, INFO_HACKER)

    return info(request, SUCCESS)

def getHomeworkStatu(request, hsid):
    hs = get_object_or_404(HomeworkStatu, pk=hsid)
    try:
        c = Course.objects.get(pk=hs.cid)
    except:
        return info(request, INFO_DB_ERR)

    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp

    # check privilege
    try:
        cm = CourseMember.objects.get(cid=c.pk, uid=user.pk)
    except:
        raise PermissionDenied

    hwSt = {
        'id': hs.pk,
        'cname': c.name,
        'answer': hs.answer,
        'types': hs.types,
        'status': hs.status,
        'cm_date': str(hs.commit_date)
    }
    if hs.types == 1:
        hwSt['score'] = hs.score
        hwSt['comment'] = hs.comment

    data = {
        'hs': hwSt
    }

    # return
    if request.method == 'GET':
        if cm.types<3:
            return render(request, 'homeworkStatus/hsM.html', data)
        if hs.uid == user.pk:
            return render(request, 'homeworkStatus/hsS.html', data)
        raise PermissionDenied
    elif request.method == 'POST':
        return info(request, 0, 'POST')
        # TODO: check M/S?
        return info(request, 0, 'TODO')
    else:
        raise PermissionDenied

def scoreHomework(request, hsid):
    if request.method != 'POST':
        raise PermissionDenied

    # get hs u c cm
    hs = HomeworkStatu.objects.filter(pk=hsid)
    if not hs.exists():
        return info(request, INFO_HACKER)
    hs = hs[0]

    crd_st, rd = checkReqData(request, post=['score', 'comment'])
    if crd_st == -1:
        return rd
    # check score (>0)
    if int(request.POST['score'])<0 or int(request.POST['score'])>100:
        return info(request, INFO_HACKER)

    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp

    try:
        c = Course.objects.get(pk=hs.cid)
    except:
        return info(request, INFO_DB_ERR)

    cm = CourseMember.objects.filter(cid=c.pk, uid=user.pk)
    if not cm.exists():
        return info(request, INFO_HACKER)
    cm = cm[0]

    # check privilege
    if cm.types >= 3:
        return info(request, INFO_HACKER)

    try:
        hs.score = int(request.POST['score'])
        hs.comment = request.POST['comment']
        hs.types = 1
        hs.save()
    except:
        return info(request, INFO_DB_ERR)

    return info(request, SUCCESS)
