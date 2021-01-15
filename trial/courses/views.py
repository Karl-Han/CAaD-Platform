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
    popularCourse10 = Course.objects.order_by('-popularity')[:10]
    data = {
        'pcourses': popularCourse10
    }
    return render(request, 'index/index.html', data)

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

    course = Course.objects.filter(name=request.POST['name'])
    if course.exists():
        data = {
            'status': -5,
            'reason': 'Course with same name exists!'
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
        data = {
            'status': -9,
            'reason': 'Database error!'
            #'debug': str(e)
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # do add privilege
    try:
        cm = CourseMember(
            cid = c.pk,
            uid = user.pk,
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
    if st == -2:
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

    # has pricilege (TODO: admin|normal)
    try:
        creator = User.objects.get(pk=course.ctrid)
    except:
        data = {
            'status': -5,
            'reason': 'Database error!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # Views++ -> popularity++
    course.popularity += 1  # TODO: limit user and ip
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
    # checks
    try:
        request.POST['password']
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

    course = get_object_or_404(Course, name=cname)
    cm = CourseMember.objects.filter(uid=user.pk, cid=course.pk)
    if cm.exists():
        data = {
            'status': -5,
            'reason': 'Added. Please refresh!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # TODO: password length & char check
    if course.password != request.POST['password']:
        data = {
            'status': 2,
            'reason': 'Wrong password'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # do add privilege
    try:
        cm = CourseMember(
            cid = course.pk,
            uid = user.pk,
            types = 3  # default: student
        )
        cm.save()
    except:
        data = {
            'status': -9,
            'reason': 'Database error!',
        }


    data = {
        'status': 1,
        'reason': 'success'
    }
    return render(request, 'info.html', {'info': json.dumps(data)})


