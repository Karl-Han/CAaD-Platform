import os
from Crypto.Hash import SHA3_512

def genToken(nickname):
    hObj = SHA3_512.new()
    hObj.update(bytes(nickname, 'utf8')+os.urandom(32))
    token = hObj.hexdigest()
    return token
