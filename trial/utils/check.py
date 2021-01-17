from django.shortcuts import render
from django.utils import timezone

from users.models import User

from Crypto.Hash import SHA3_512
import json
import os

class Visitor:
    nickname = 'Visitor'
    token = 'None'

TTO = 7200  # token timeout (seconds)

def info(request, st, reason, debug=None):
    if debug == None:
        data = {
            'status': st,
            'reason': reason
        }
        return render(request, 'info.html', {'info': json.dumps(data)})
    else:
        data = {
            'status': st,
            'reason': reason,
            'debug': debug
        }
        return render(request, 'info.html', {'info': json.dumps(data, indent=4, sort_keys=True, default=str)})

def isTokenTimeout(user):
    return (timezone.now()-user.last_login).seconds > TTO

def checkTokenTimeoutOrLogout(user):
    if len(user.token) != 128:
        return False
    result = isTokenTimeout(user)
    if result:
        # do logout
        hObj = SHA3_512.new()
        hObj.update(bytes(user.nickname, 'utf8')+os.urandom(32))
        token = hObj.hexdigest()
        user.token = token[:-2]  # len->126, reduce database operations
        user.save()  # except?
    return result

def checkUserLoginOrVisitor(request):
    if (not 'utk' in request.COOKIES) or len(request.COOKIES['utk'])!=128:
        return -1, Visitor()

    user = User.objects.filter(token=request.COOKIES['utk'])
    if not user.exists():
        return -2, Visitor()

    user = user[0]
    return 1, user

def checkReqData(request, post=[], cookies=[]):
    try:
        for p in post:
            request.POST[p]
        for c in cookies:
            request.COOKIES[c]
        return 1, None
    except:
        return -1, info(request, -1, 'Hacker? 110!')

def checkUser(request):
    culv_st, user = checkUserLoginOrVisitor(request)
    if culv_st == -1:
        return -2, info(request, -2, 'Please login!')
    elif culv_st == -2:  # user not exitst
        return -3, info(request, -3, 'Hacker?110!')

    if checkTokenTimeoutOrLogout(user):
        return -4, info(request, -4, 'Please login!')
    return 1, user

