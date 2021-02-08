from users.models import User
from homeworks.models import HomeworkStatu
from files.models import FileHomework

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

