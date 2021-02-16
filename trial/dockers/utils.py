import zipfile
import socket
import random
import os
import shutil
from files.models import FileDocker
from trial.settings import BASE_DIR
from Crypto.Hash import SHA3_256

# return Dockerfile path
def unzip(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for n in fz.namelist():
            if 'Dockerfile' in n:
                pth = n
                break
        else:
            return False
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        return pth
    return False

def rmDockerDir(hid):
    dst = os.path.join(BASE_DIR, 'media/docker/%d/'%hid)
    shutil.rmtree(dst)

def checkPort(port, host):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, int(port)))
        return True
    except socket.error:
        return False
    finally:
        if s:
            s.close()

def randPort(lb=1025, ub=65535):
    return random.randrange(lb, ub)

def isSameFile(f1, f2):
    if f1==f2:
        return True
    f1.open()
    f2.open()
    hObj = SHA3_256.new()
    hObj.update(f1.read())
    hash1 = hObj.hexdigest()
    hObj.update(f2.read())
    hash2 = hObj.hexdigest()
    f1.close()
    f2.close()
    return hash1==hash2
