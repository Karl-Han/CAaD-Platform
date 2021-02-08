from django.shortcuts import render
from django.utils import timezone

from users.models import User

from Crypto.Hash import SHA3_512
import json
import os

from utils.status import *

class Visitor:
    nickname = 'Visitor'
    token = 'None'

TTO = 7200  # token timeout (seconds)

def info(request, st, reason=None, debug=None):
    if reason == None:
        try:
            reason = INFO_STR[st]
        except:
            reason = 'Inner Error! St not found!'

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

def checkReqData(request,  **kwargs):
    post = kwargs.pop('post', [])
    cookies = kwargs.pop('cookies', [])
    files = kwargs.pop('files', [])
    try:
        for p in post:
            request.POST[p]
        for c in cookies:
            request.COOKIES[c]
        for f in files:
            request.FILES[f]
        return 1, None
    except:
        return -1, info(request, INFO_HACKER)

def checkUser(request):
    culv_st, user = checkUserLoginOrVisitor(request)
    if culv_st == -1:
        return -2, info(request, INFO_LOGIN)
    elif culv_st == -2:  # user not exitst
        return -3, info(request, INFO_HACKER)

    if checkTokenTimeoutOrLogout(user):
        return -4, info(request, INFO_LOGIN)
    return 1, user

