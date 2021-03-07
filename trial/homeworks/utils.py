from users.models import User
from homeworks.models import HomeworkStatu
from files.models import FileHomework
from dockers.models import DockerStatu
from utils.parms import DOCKER_SERVER_HOST

def getHs(hid):
    hwSt = HomeworkStatu.objects.filter(hid=hid)
    hs = []
    for _hs in hwSt:
        uname = User.objects.get(pk=_hs.uid).nickname
        hs.append({
            'id': _hs.pk,
            'types': _hs.types,
            'uname': uname
        })
    return hs

def getFh(hid):
    fhs = FileHomework.objects.filter(hid=hid)
    fh = []
    for _fh in fhs:
        fh.append({
            'name': ''.join(_fh.file.name.split('/')[4:]),
            'url': _fh.file.url
        })
    return fh

def getDk(hid):
    try:
        dk = DockerStatu.objects.get(hid=hid)
    except:
        return None
    data = {
        'host': DOCKER_SERVER_HOST,
        'port': dk.oport,
        'status': dk.status
    }
    return data
