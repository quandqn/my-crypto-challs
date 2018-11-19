import base64
from Crypto.Cipher import AES
from hashlib import md5
import os

class AES_(object):

    def __init__(self, key):
        self.blocksize = 16
        self.key = md5(key).digest()

    def pad(self, st):
        return st + (self.blocksize - len(st) % self.blocksize) * chr(self.blocksize - len(st) % self.blocksize)

    def unpad(self, st):
        return st[:-ord(st[len(st)-1:])]

    def encrypt(self, msg):
        msg = self.pad(msg)
        iv = os.urandom(16)
        crypt = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode((iv + crypt.encrypt(msg))).decode('utf-8')

    def decrypt(self, msg):
        msg = base64.b64decode(msg)
        iv = msg[:self.blocksize]
        crypt = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(crypt.decrypt(msg[self.blocksize:])).decode('utf-8')
