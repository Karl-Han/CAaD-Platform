from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from users.models import User
from courses.models import Course, CourseMember
from homeworks.models import Homework, HomeworkStatu

import json
import random

from utils.check import info, Visitor, checkTokenTimeoutOrLogout, checkUserLoginOrVisitor, checkReqData, checkUser
from utils.status import *
from .utils import getRandCPwd, getCM, getHw

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
        return info(request, INFO_SAME_NAME, INFO_STR[INFO_SAME_NAME]%('Course', 'name'))

    # do create
    data = {
        'name': request.POST['name'],
        'password': getRandCPwd(),
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
        return info(request, INFO_DB_ERR)

    # do add privilege
    try:
        cm = CourseMember(
            cid = c.pk,
            uid = user.pk,
            types = 0  # creator is admin
        )
        cm.save()
    except:
        return info(request, INFO_DB_ERR)

    # success
    data = {
        'status': 1,
        'reason': 'success',
        'href': '/courses/'+c.name
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

def coursePage(request, cname):
    course = get_object_or_404(Course, name=cname)

    st, user = checkUserLoginOrVisitor(request)
    # check user
    if st == -2:  # user not exitst
        return info(request, INFO_HACKER)

    if checkTokenTimeoutOrLogout(user):
        st = -1  # visistor

    # has pricilege (TODO: admin|normal)
    try:
        creator = User.objects.get(pk=course.ctrid)
    except:
        return info(request, INFO_DB_ERR)

    # Views++ -> popularity++
    course.popularity += 1  # TODO: limit user and ip
    try:
        course.save()
    except:
        return info(request, INFO_DB_ERR)

    try:
        cm = getCM(course.pk)
    except:
        return info(request, INFO_DB_ERR)

    try:
        hw = getHw(course.pk)
    except:
        return info(request, INFO_DB_ERR)

    data = {
        'course': course,
        'creator': creator,
        'cm': cm,
        'hw': hw
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
        return info(request, WA_PWD)

    # do add privilege
    try:
        cm = CourseMember(
            cid = course.pk,
            uid = user.pk,
            types = 3  # default: student
        )
        cm.save()
    except:
        return info(request, INFO_DB_ERR)

    return info(request, SUCCESS)

def doChangePwd(request, cname):
    if request.method != 'POST':
        raise PermissionDenied

    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp

    c = get_object_or_404(Course, name=cname)
    cm = get_object_or_404(CourseMember, uid=user.pk, cid=c.pk)
    hasPriv = [0, 1]
    if not cm.types in hasPriv:
        raise PermissionDenied

    pwd = getRandCPwd()
    try:
        c.password = pwd
        c.save()
    except:
        return info(request, INFO_DB_ERR)

    # success
    data = {
        'status': 1,
        'reason': 'success',
        'pwd2': pwd
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

def doDelUser(request, cname, uname):
    if request.method != 'POST':
        raise PermissionDenied
    c = get_object_or_404(Course, name=cname)

    # check privilege
    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp
    try:
        cm = CourseMember.objects.get(cid=c.pk, uid=user.pk)
    except:
        return info(request, INFO_DB_ERR)
    if cm.types >= 3:
        raise PermissionDenied

    # get cm
    du = get_object_or_404(User, nickname=uname)
    try:
        dcm = CourseMember.objects.get(cid=c.pk, uid=du.pk)
    except:
        return info(request, INFO_DB_ERR)

    if cm.types >= dcm.types:  # TODO: delete itself
        raise PermissionDenied

    # do delete
    try:
        dcm.delete()
    except:
        return info(request, INFO_DB_ERR)

    # del hs
    hs = HomeworkStatu.objects.filter(uid=du.pk, cid=c.pk)
    try:
        for i in hs:
            i.delete()
    except:
        return info(request, INFO_DB_ERR)

    return info(request, SUCCESS)

def doChgUserPriv(request, cname, uname):
    if request.method != 'POST':
        raise PermissionDenied
    # checks
    crd_st, rd = checkReqData(request, post=['priv2'])
    if crd_st == -1:
        return rd
    mp = {'adm':0, 'tea':1, 'asi':2, 'stu':3}
    try:
        priv2 = mp[request.POST['priv2']]
    except:
        return info(request, INFO_HACKER)

    c = get_object_or_404(Course, name=cname)

    # check privilege
    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp
    try:
        cm = CourseMember.objects.get(cid=c.pk, uid=user.pk)
    except:
        return info(request, INFO_DB_ERR)
    if cm.types >= 3:
        raise PermissionDenied

    # get cm and check
    cu = get_object_or_404(User, nickname=uname)
    if user.pk == cu.pk:
        return info(request, INFO_CANTB_SELF, INFO_STR[INFO_CANTB_SELF]%'User')
    try:
        ccm = CourseMember.objects.get(cid=c.pk, uid=cu.pk)
    except:
        return info(request, INFO_DB_ERR)
    if cm.types >= ccm.types:
        raise PermissionDenied
    if ccm.types == priv2:
        return info(request, INFO_CANTB_SAME, INFO_STR[INFO_CANTB_SAME]%'Privilege')
    if cm.types >= priv2:
        raise PermissionDenied

    # change
    try:
        ccm.types = priv2
        ccm.save()
    except:
        return info(request, INFO_DB_ERR)

    return info(request, SUCCESS)
