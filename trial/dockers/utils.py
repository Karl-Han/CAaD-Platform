import zipfile
import socket
import random
import os
import shutil
from Crypto.Hash import SHA3_256

# from files.models import FileDocker
from trial.settings import BASE_DIR

def unzip(file_path, dst):
    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            if 'Dockerfile' in zip_ref.namelist():
                zip_ref.extractall(dst)
                return True
    return False

def get_rand_available_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    unavailable_ports = []

    while True:
        port = random.randrange(1025, 65525)
        location = ("0.0.0.0", port)

        result_of_check = a_socket.connect_ex(location)
        if result_of_check == 0:
            # Port is open
            pass
        else:
            # Port is not open
            if port not in unavailable_ports:
                return port
            unavailable_ports.append(port)

def get_docker_client():
    return DockerClient(base_url=DOCKER_BASE_URL)