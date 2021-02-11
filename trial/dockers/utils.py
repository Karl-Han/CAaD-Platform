import zipfile
import socket
import random
from files.models import FileDocker

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
