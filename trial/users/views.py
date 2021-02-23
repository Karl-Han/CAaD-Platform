from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views import View
from django.db import IntegrityError


from users.models import User
from courses.models import Course, CourseMember
from users.form import UserForm

from Crypto.Hash import SHA3_512
import json

from utils.check import info, Visitor, checkTokenTimeoutOrLogout, checkReqData, checkUser
from utils.status import *
from .utils import genToken

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. <a href=\"/users/login\">login</a>")

class SignupView(View):
    template_name = 'signup/signup.html'

    def get(self, request):
        if context == None:
            context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserForm(request.POST)

        if request.POST['password'] != request.POST['password2']:
            return info(request, INFO_NOT_MATCH, INFO_STR[INFO_NOT_MATCH]%'Password')

        if form.is_valid():
            # Check on 
            # * valid of email
            # * unique of nickname and email

            form.cleaned_data['privilege'] = 5
            form.cleaned_data['status'] = SU_NORMAL
            form.cleaned_data['token'] = ''
            form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
            
            form.save()
            return HttpResponseRedirect(reverse("users:user_index"))
        else:
            # ToDo: 
            # display error in the signup page and restore nickname and email
            print("ERROR in form")
            errors = []
            context = {}
            for field in form:
                errors.append(str(field.errors))
            error_str = '\n'.join(errors)
            context['nickname'] = request.POST['nickname']
            context['email'] = request.POST['email']
            context['error_message'] = error_str
            # return render(request, self.template_name, {'error_message': error_str})
            return HttpResponseRedirect(reverse('users:signup', kwargs=context))

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
        return info(request, WA_PWD2)

    user = user[0]  # should be unique
    if not check_password(request.POST['password'], user.password): # password not match
        return info(request, WA_PWD2)

    # get token (random)
    user.token = genToken(user.nickname)
    user.last_login = timezone.now()
    try:
        user.save()
    except:
        return info(request, INFO_DB_ERR)

    # success
    data = {
        'status': 1,
        'data': {
            'token': user.token,
            'href': '/users/'+user.nickname  # TODO: abstract users here
        }
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

def getUC(user):  # get courses joined in 
    cmem = CourseMember.objects.filter(uid=user.pk)
    uc = []
    for cm in cmem:
        course = Course.objects.get(pk=cm.cid)
        uc.append({
            'cname': course.name,
            'cpopularity': course.popularity,
            'uprivilege': cm.types
        })
    return uc

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
                try:
                    uc = getUC(user)
                except:
                    return info(request, INFO_DB_ERR)
                data = {
                    'user': user,
                    'uc': uc
                }
                return render(request, 'profile/self.html', data)
        except:
            return info(request, INFO_UNKNOW)
    else:
        data = {
            'user': user,
            'owner': owner
        }
        return render(request, 'profile/other.html', data)