from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from users.models import User
from courses.models import Course, CourseMember

import json
import random

from utils.check import info, Visitor, checkTokenTimeoutOrLogout, checkUserLoginOrVisitor, checkReqData, checkUser
from utils.status import *

# Create your views here.
def index(request):
    popularCourse10 = Course.objects.order_by('-popularity')[:10]
    data = {
        'pcourses': popularCourse10
    }
    return render(request, 'index/index.html', data)

def createCourse(request):
    return render(request, 'create/create.html', {})

def doCreate(request):
    if request.method != 'POST':
        raise PermissionDenied

    # checks
    crd_st, rd = checkReqData(request, post=['name', 'description'])
    if crd_st == -1:
        return rd

    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp

    course = Course.objects.filter(name=request.POST['name'])
    if course.exists():
        return info(request, INFO_SAME_NAME, 'Course'+INFO_STR[INFO_SAME_NAME])

    # do create
    data = {
        'name': request.POST['name'],
        'password': ''.join(random.sample('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', 8)),
        'ctrid': user.id,
        'description': request.POST['description'],
        'status': 0,
        'types': 0,  # reserved
        'create_date': timezone.now(),
        'popularity': 0
    }
    #return render(request, 'info.html', {'info': json.dumps(data, indent=4, sort_keys=True, default=str)})  # debug
    try:
        c = Course(
            name = data['name'],
            password = data['password'],
            ctrid = data['ctrid'],
            description = data['description'],
            status = data['status'],
            types = data['types'],
            create_date = data['create_date'],
            popularity = data['popularity']
        )
        c.save()
    except Exception as e:
        return info(request, INFO_DB_ERR, INFO_STR[INFO_DB_ERR])

    # do add privilege
    try:
        cm = CourseMember(
            cid = c.pk,
            uid = user.pk,
            types = 0  # creator is admin
        )
        cm.save()
    except:
        return info(request, INFO_DB_ERR, INFO_STR[INFO_DB_ERR])

    # success
    data = {
        'status': 1,
        'reason': 'success',
        'href': '/courses/'+c.name
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

def getCM(cid):
    cmem = CourseMember.objects.filter(cid=cid)
    cm = []
    for c in cmem:
        uid = c.uid
        user = User.objects.get(pk=uid)
        cm.append({
            'uname': user.nickname,
            'uprivilege': c.types
        })
    return cm

def coursePage(request, cname):
    course = get_object_or_404(Course, name=cname)

    st, user = checkUserLoginOrVisitor(request)
    # check user
    if st == -2:  # user not exitst
        return info(request, INFO_HACKER, INFO_STR[INFO_HACKER])

    if checkTokenTimeoutOrLogout(user):
        st = -1  # visistor

    # has pricilege (TODO: admin|normal)
    try:
        creator = User.objects.get(pk=course.ctrid)
    except:
        return info(request, INFO_DB_ERR, INFO_STR[INFO_DB_ERR])

    # Views++ -> popularity++
    course.popularity += 1  # TODO: limit user and ip
    try:
        course.save()
    except:
        return info(request, INFO_DB_ERR, INFO_STR[INFO_DB_ERR])

    try:
        cm = getCM(course.pk)
    except:
        return info(request, INFO_DB_ERR, INFO_STR[INFO_DB_ERR])

    data = {
        'course': course,
        'creator': creator,
        'cm': cm
    }

    # check privilege
    if st == -1:  # visitor
        return render(request, 'course/courseV.html', data)  # visitor

    cmember = CourseMember.objects.filter(cid=course.pk)
    cmember = cmember.filter(uid=user.pk)
    if not cmember.exists():
        return render(request, 'course/courseV.html', data)  # visitor

    cm = cmember[0]  # only one!
    if cm.types==0:    # admin
        return render(request, 'course/courseA.html', data)
    elif cm.types==1:  # teacher
        return render(request, 'course/courseT.html', data)
    elif cm.types==2:  # asistant
        return render(request, 'course/courseAs.html', data)
    elif cm.types==3:  # student
        return render(request, 'course/courseS.html', data)

def doJoin(request, cname):
    if request.method != 'POST':
        raise PermissionDenied

    # checks
    crd_st, rd = checkReqData(request, post=['password'])
    if crd_st == -1:
        return rd

    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp

    course = get_object_or_404(Course, name=cname)
    cm = CourseMember.objects.filter(uid=user.pk, cid=course.pk)
    if cm.exists():
        return info(request, INFO_REFRESH, 'Added. '+INFO_STR[INFO_REFRESH])

    # TODO: password length & char check
    if course.password != request.POST['password']:
        return info(request, WA_PWD, INFO_STR[WA_PWD])

    # do add privilege
    try:
        cm = CourseMember(
            cid = course.pk,
            uid = user.pk,
            types = 3  # default: student
        )
        cm.save()
    except:
        return info(request, INFO_DB_ERR, INFO_STR[INFO_DB_ERR])

    return info(request, SUCCESS, INFO_STR[SUCCESS])


