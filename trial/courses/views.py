from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

from users.models import User
from users.views import Visitor, checkTokenTimeoutOrLogout, checkUserLoginOrVisitor
from courses.models import Course, CourseMember

import json
import random

# Create your views here.
def index(request):
    return render(request, 'index/index.html', {})

def createCourse(request):
    return render(request, 'create/create.html', {})

def doCreate(request):
    # checks
    try:
        request.POST['name']
        request.POST['description']
    except:
        data = {
            'status': -1,
            'reason': 'Hacker? 110!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    st, user = checkUserLoginOrVisitor(request)
    if st == -1:
        data = {
            'status': -2,
            'reason': 'Please login!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})
    elif st == -2:
        data = {
            'status': -3,
            'reason': 'Hacker?110!'  # user not exitst
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    if checkTokenTimeoutOrLogout(user):
        data = {
            'status': -4,
            'reason': 'Please login!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # do create
    data = {
        'name': request.POST['name'],
        'password': ''.join(random.sample('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', 8)),
        'ctrid': user.id,
        'description': request.POST['description'],
        'status': 0,
        'types': 0,  # reserved
        'create_date': timezone.now(),
        'hot': 0
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
            hot = data['hot']
        )
        c.save()
    except Exception as e:
        data = {
            'status': -9,
            'reason': 'Database error!'
            #'debug': str(e)
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # do add privilege
    try:
        cm = CourseMember(
            cid = c.id,
            uid = user.id,
            types = 0  # creator is admin
        )
        cm.save()
    except:
        data = {
            'status': -10,
            'reason': 'Database error!',
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # success
    # TODO: test and debug here(1.13)
    data = {
        'status': 1,
        'reason': 'success',
        'href': '/courses/'+c.name
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

    # Something strang happened
    data = {
        'status': 0,
        'reason': '???'
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

def coursePage(request, cname):
    course = get_object_or_404(Course, name=cname)
    st, user = checkUserLoginOrVisitor(request)
    # check user
    if st == -1:  # visitor
        return render(request, 'course/reject.html', {})
    elif st == -2:
        data = {
            'status': -3,
            'reason': 'Hacker?110!'  # user not exitst
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    if checkTokenTimeoutOrLogout(user):
        data = {
            'status': -4,
            'reason': 'Please login!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # check privilege
    cmember = CourseMember.objects.filter(cid=course.pk)
    if not cmember.filter(uid=user.pk).exists():
        return render(request, 'course/reject.html', {})

    # has pricilege (TODO: admin|normal)
    try:
        creator = User.objects.get(pk=course.ctrid)
    except:
        data = {
            'status': -5,
            'reason': 'Database error!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # Views++ -> hot++
    course.hot += 1
    try:
        course.save()
    except:
        data = {
            'status': -6,
            'reason': 'Database error!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    data = {
        'course': course,
        'creator': creator
    }
    return render(request, 'course/course.html', data)


