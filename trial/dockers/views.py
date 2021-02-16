from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from users.models import User
from homeworks.models import Homework
from courses.models import Course, CourseMember
from files.models import FileDocker
from .models import DockerStatu

import json
import docker

from utils.check import info, checkReqData, checkUser
from utils.status import *
from utils.parms import DOCKER_SERVER_URL, DOCKER_NAME_PRE
from .utils import unzip, checkPort, randPort, rmDockerDir, isSameFile

# Create your views here.
def index(request):
    return HttpResponse("403.")

# TODO: delete all before push - -
def createDocker(request):
    if request.method != 'POST':
        raise PermissionDenied

    crd_st, rd = checkReqData(request, post=['hid', 'iport'], files=['dfile'])
    if crd_st == -1:
        return rd
    try:
        hid = int(request.POST['hid'])
        iport = int(request.POST['iport'])
    except:
        return info(request, INFO_HACKER)

    # check u
    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp

    # check cm
    try:
        h = Homework.objects.get(pk=hid)
        c = Course.objects.get(pk=h.cid)
        cm = CourseMember.objects.get(cid=c.pk, uid=user.pk)
    except:
        return info(request, INFO_HACKER)
    if cm.types >= 3:
        return info(request, INFO_HACKER)

    # fd
    try:
        fd = FileDocker.objects.get(hid=hid)
        # TODO: check dup
    except:
        try:
            fd = FileDocker(
                uid = user.pk,
                create_date = timezone.now(),
                hid = hid,
                file = request.FILES['dfile']
            )
            fd.file.name = '%d.zip'%hid
            fd.save()
        except:
            return info(request, INFO_DB_ERR)

    # unzip
    uzsrc = fd.file.path
    uzdst = '/'.join(uzsrc.split('/')[:-1])+'/%d/'%hid
    df_pth = unzip(uzsrc, uzdst)
    if df_pth == False:
        return info(request, INFO_UNZIP_ERR)
    df_pth = uzdst+'/'.join(df_pth.split('/')[:-1])+'/'

    # build image
    tag_name = DOCKER_NAME_PRE+str(hid)
    c = docker.Client(base_url=DOCKER_SERVER_URL)

    ds = DockerStatu.objects.filter(hid=hid)
    if ds.exists():
        # building
        if ds.status == 1:
            return info(request, INFO_CTRING)
        # do delete old images and containers and set default
        ds = ds[0]
        if ds.ctnid != '':
            c.remove_container(container=ds.ctnid)
            ds.ctnid = ''
        if ds.imgid != '':
            c.remove_image(image=ds.imgid)
            ds.imgid = ''
        ds.iport = -1
        ds.oport = -1
        ds.status = 0
        try:
            ds.save()
        except:
            return info(request, INFO_DB_ERR)
    else:
        try:
            ds = DockerStatu(
                ctrid = user.pk,
                hid = hid,
                name = tag_name,
                ctnid = '',  # to be create
                imgid = '',
                iport = iport,
                oport = -1,
                types = 0,
                status = 1,
                create_date = timezone.now(),
                update_date = timezone.now()
            )
            ds.save()
        except:
            return info(request, INFO_DB_ERR)

    response = [line for line in c.build(
        path=df_pth,
        rm=True,
        tag=tag_name
    )]
    try:
        rmDockerDir(hid)
    except:
        return info(request, INFO_OS_ERR)

    # check success
    dk_chk = json.loads(response[-1])
    if 'errorDetail' in dk_chk:
        try:
            for im in c.images():
                # Suppose all images have tags
                if im['RepoTags'] == ['<none>:<none>']:
                    iid = im['Id'][7:19]
                    c.remove_image(image=iid)
        except:
            return info(request, INFO_UNKNOW)

        try:
            ds.status = 2
            ds.save()
        except:
            return info(request, INFO_DB_ERR)
    elif 'stream' in dk_chk and 'Successfully tagged ' in dk_chk['stream']:
        im = c.images(tag_name)
        if im != []:  # success
            try:
                ds.imgid = im[0]['Id'][7:]
                ds.save()
            except:
                return info(request, INFO_DB_ERR)
        else:         # fail
            try:
                ds.status = 0
                ds.save()
            except:
                return info(request, INFO_DB_ERR)
            return info(request, INFO_UNKNOW)  # check if happened ...

    # create container
    oport = randPort()
    container = c.create_container(
        image=tag_name,
        name=tag_name,
        detach=True,
        ports=[iport],
        host_config=c.create_host_config(port_bindings={iport:oport})
    )
    ctnid = container['Id']
    c.start(container=ctnid)

    try:
        ds.ctnid = ctnid
        ds.oport = oport
        ds.status = 3
        ds.update_date = timezone.now()
        ds.save()
    except:
        return info(request, INFO_DB_ERR)

    data = {
        'status': 1,
        'oport': oport
    }
    return render(request, 'info.html', {'info': json.dumps(data)})

def deleteDocker(request):
    if request.method != 'POST':
        raise PermissionDenied

    crd_st, rd = checkReqData(request, post=['hid'])
    if crd_st == -1:
        return rd
    try:
        hid = int(request.POST['hid'])
    except:
        return info(request, INFO_HACKER)

    # check u
    cu_st, tmp = checkUser(request)
    if not cu_st == 1:
        return tmp
    user = tmp

    # check cm
    try:
        h = Homework.objects.get(pk=hid)
        c = Course.objects.get(pk=h.cid)
        cm = CourseMember.objects.get(cid=c.pk, uid=user.pk)
    except:
        return info(request, INFO_HACKER)
    if cm.types >= 3:
        return info(request, INFO_HACKER)

    # del fd
    try:
        fd = FileDocker.objects.get(hid=hid)
    except:
        return info(request, INFO_DB_ERR)
    fd.file.delete()
    fd.delete()

    # get ds
    c = docker.Client(base_url=DOCKER_SERVER_URL)
    try:
        ds = DockerStatu.objects.get(hid=hid)
        ds.status = 5  # lock
        ds.save()
    except:
        return info(request, INFO_DB_ERR)

    # del container
    c.remove_container(container=ds.ctnid)
    try:
        ds.ctnid = ''
        ds.save()
    except:
        return info(request, INFO_DB_ERR)

    # del image
    c.remove_image(image=ds.imgid)
    try:
        ds.imgid = ''
        ds.save()
    except:
        return info(request, INFO_DB_ERR)

    # 
    try:
        ds.delete()
    except:
        return info(request, INFO_DB_ERR)

    return info(request, SUCCESS)

# TODO: update (use signals)
