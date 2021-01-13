from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from users.models import User

from Crypto.Hash import SHA3_512
import json
import os

TTO = 7200  # token timeout (seconds)

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def signup(request):
    context = {}
    return render(request, 'signup/signup.html', context)

def doSignup(request):
    # POST payload check
    try:
        request.POST['userName']
        request.POST['password']
        request.POST['password2']
        request.POST['email']
        request.POST['realName']
        request.POST['uid']
    except:
        data = {
            'status': -1,
            'reason': 'Hacker? 110!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    if request.POST['password'] != request.POST['password2']:
        data = {
            'status': -2,
            'reason': 'Password not match!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

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
        data = {
            'status': -3,
            'reason': 'User with same name existed!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    u = User.objects.filter(email=data['email']);
    if u.exists():
        data = {
            'status': -4,
            'reason': 'User with same email existed!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # TODO: more checks here (safer password & email format)
    # save to database
    try:
        u = User(  # TODO: error here
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
        data = {
            'status': 1,
            'reason': 'success'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})
    except Exception as e:
        data = {
            'status': -9,
            'reason': 'Database error!',
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # Something strang happened
    data = {
        'status': 0,
        'reason': '???'
    }
    return render(request, 'info.html', {'info': json.dumps(data)})
    #return render(request, 'info.html', {'info': json.dumps(data, indent=4, sort_keys=True, default=str)})  # TODO: write database and remove str


def login(request):
    context = {}
    return render(request, 'login/login.html', context)

def doLogin(request):
    # POST payload check
    try:
        request.POST['name']
        request.POST['password']
    except:
        data = {
            'status': -1,
            'reason': 'Hacker? 110!'
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    user = User.objects.filter(nickname=request.POST['name'])
    if not user.exists():
        data = {
            'status': -2,
            'reason': 'Wrong user name or password'  # user not exitst
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    user = user[0]  # should be unique
    if not check_password(request.POST['password'], user.password):
        data = {
            'status': -3,
            'reason': 'Wrong user name or password'  # password not match
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # get token (random)
    hObj = SHA3_512.new()
    hObj.update(bytes(user.nickname, 'utf8')+os.urandom(32))
    token = hObj.hexdigest()
    user.token = token
    try:
        user.last_login = timezone.now()
        user.save()
    except:
        data = {
            'status': -9,
            'reason': 'Database error!',
        }
        return render(request, 'info.html', {'info': json.dumps(data)})

    # success
    data = {
        'status': 1,
        'data': {
            'token': token,
            'href': '/users/'+user.nickname  # TODO: abstract users here
        }
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

    # Something strang happened
    data = {
        'status': 0,
        'reason': '???'
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

def isTokenTimeout(user):
    return (timezone.now()-user.last_login).seconds > TTO

class Visitor:
    nickname = 'Visitor'
    token = 'None'

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
        if isTokenTimeout(user):
            # do logout
            hObj = SHA3_512.new()
            hObj.update(bytes(user.nickname, 'utf8')+os.urandom(32))
            token = hObj.hexdigest()
            user.token = token[:-2]  # len->126, reduce database operations
            try:
                user.save()
            except:
                data = {
                    'status': -9,
                    'reason': 'Something wrong, please contact developer',
                }
                return render(request, 'info.html', {'info': json.dumps(data)})
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
    else:
        data = {
            'user': user,
            'owner': owner
        }
        return render(request, 'profile/other.html', data)

