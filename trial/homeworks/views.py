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

# Create your views here.
def index(request):
    return HttpResponse("test")

def doCreate(request):
    if request.method != 'POST':
        raise PermissionDenied

    crd_st, rd = checkReqData(request, post=['cname', 'title', 'description', 'tips', 'answer', 'runsec'])  # TODO: docker
    if crd_st == -1:
        return rd

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
        if cm.types >= 2:  # not admin or teacher
            raise PermissionDenied
    except:
        return info(request, INFO_HACKER)

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
    # get and check
    return info(request, 0, 'test')

    if request.method != 'GET':
        pass
    elif request.method != 'POST':
        pass
    else:
        raise PermissionDenied
