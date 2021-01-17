from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from users.models import User
from courses.models import Course, CourseMember

from Crypto.Hash import SHA3_512
import json
import os

from utils.check import info, Visitor, checkTokenTimeoutOrLogout, checkReqData, checkUser

class Visitor:
    nickname = 'Visitor'
    token = 'None'

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def signup(request):
    context = {}
    return render(request, 'signup/signup.html', context)

def doSignup(request):
    if request.method != 'POST':
        raise PermissionDenied

    # POST payload check
    crd_st, rd = checkReqData(request, post=['userName', 'password', 'password2', 'email', 'realName', 'uid'])
    if crd_st == -1:
        return rd

    if request.POST['password'] != request.POST['password2']:
        return info(request, -2, 'Password not match!')

    data = {
        'nickname': request.POST['userName'],
        'password': make_password(request.POST['password'], salt=None, hasher='default'),
        'email': request.POST['email'],
        'realname': request.POST['realName'],
        'uid': request.POST['uid'],
        'privilege': 5,
        'status': 1,  # TODO: email activatived
        'signup_date': timezone.now(),
        'last_login': timezone.now(),
        'token': '',  # TODo: activity code here
    }

    # same name & email
    # TODO: add sameName checker(check in time!)
    u = User.objects.filter(nickname=data['nickname']);
    if u.exists():
        return info(request, -3, 'User with same name existed!')

    u = User.objects.filter(email=data['email']);
    if u.exists():
        return info(request, -4, 'User with same email existed!')

    # TODO: more checks here (safer password & email format)
    # save to database
    try:
        u = User(
            nickname = data['nickname'],
            password = data['password'],
            email = data['email'],
            realname = data['realname'],
            uid = data['uid'],
            privilege = data['privilege'],
            status = data['status'],
            signup_date = data['signup_date'],
            last_login = data['last_login'],
            token = data['token']
        )
        u.save()
        return info(request, 1, 'success')
    except Exception as e:
        return info(request, -9, 'Database error!')

    #return render(request, 'info.html', {'info': json.dumps(data, indent=4, sort_keys=True, default=str)})  # TODO: write database and remove str

def login(request):
    context = {}
    return render(request, 'login/login.html', context)

def doLogin(request):
    if request.method != 'POST':
        raise PermissionDenied

    # POST payload check
    crd_st, rd = checkReqData(request, post=['name', 'password'])
    if crd_st == -1:
        return rd

    user = User.objects.filter(nickname=request.POST['name'])
    if not user.exists():  # user not exitst
        return info(request, -2, 'Wrong user name or password' )

    user = user[0]  # should be unique
    if not check_password(request.POST['password'], user.password): # password not match
        return info(request, -2, 'Wrong user name or password' )

    # get token (random)
    hObj = SHA3_512.new()
    hObj.update(bytes(user.nickname, 'utf8')+os.urandom(32))
    token = hObj.hexdigest()
    user.token = token
    try:
        user.last_login = timezone.now()
        user.save()
    except:
        return info(request, -9, 'Database error!')

    # success
    data = {
        'status': 1,
        'data': {
            'token': token,
            'href': '/users/'+user.nickname  # TODO: abstract users here
        }
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

def profile(request, ownerName):
    # TODO: render self or other (template)
    owner = get_object_or_404(User, nickname=ownerName)
    if 'utk' in request.COOKIES and len(request.COOKIES['utk'])==128:
        user = User.objects.filter(token=request.COOKIES['utk'])
        if not user.exists():
            user = Visitor()  # TODO: optimize
        else:
            user = user[0]
    else:
        user = Visitor()

    if user.token!='' and len(user.token)==128 and ownerName==user.nickname:
        try:
            if checkTokenTimeoutOrLogout(user):
                data = {
                    'user': Visitor(),  # logout
                    'owner': owner
                }
                return render(request, 'profile/other.html', data)
            else:
                data = {
                    'user': user
                }
                return render(request, 'profile/self.html', data)
        except:
            return info(request, -9, 'Something wrong, please contact developer')
    else:
        data = {
            'user': user,
            'owner': owner
        }
        return render(request, 'profile/other.html', data)

def getUC(request):  # get courses joined in 
    if request.method != 'POST':
        raise PermissionDenied
        #return HttpResponse('POST method only!', status=403)

    # checks
    crd_st, rd = checkReqData(request, cookies=['utk'])
    if crd_st == -1:
        return rd

    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp

    cmem = CourseMember.objects.filter(uid=user.pk)
    uc = []
    for cm in cmem:
        try:
            course = Course.objects.get(pk=cm.cid)
            uc.append({
                'cname': course.name,
                'cpopularity': course.popularity,
                'uprivilege': cm.types
            })
        except:
            return info(request, -9, 'Database error!')

    data = {
        'status': 1,
        'data': uc
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

