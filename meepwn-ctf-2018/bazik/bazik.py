#!/usr/bin/python
import random
import re
import sys
import os
from Crypto.PublicKey import RSA

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)
sys.stderr = None

menu = """	
Choose one:
1. Test the OTP
2. Get the public key
3. Get flag
"""
template = "Your OTP for transaction #731337 in ABCXYZ Bank is %i."
rsa = RSA.generate(1024, e=3)

def test_otp():
	otp = random.randint(100000000, 999999999)
	print "otp should be:", otp
	encrypted = rsa.encrypt(template % (otp), 0)[0].encode("hex")
	print "encrypted dat:", encrypted
	decrypted = rsa.decrypt(encrypted.decode("hex"))
	print "decrypted dat:", decrypted
	print "decrypted otp:", re.findall(r"\D(\d{9})\D", decrypted)

def get_public_key():
	print rsa.publickey().exportKey(format="PEM")

def get_flag():
	otp = random.randint(100000000, 999999999)
	encrypted = rsa.encrypt(template % (otp), 0)[0].encode("hex")
	print "encrypted dat:", encrypted
	decrypted = rsa.decrypt(encrypted.decode("hex"))
	_otp = re.findall(r"\D(\d{9})\D", decrypted)[0]
	inp = raw_input('send me otp to get flag >>> ')
	if inp == _otp:
		print "MeePwnCTF{blackbox-rsa-is-0xd34d}"
	else:
		print "Sorry, wrong otp. We logged this behavior and will send to #ANM for investigating."

for i in range(10):
	choice = int(raw_input(menu))
	if int(choice) == 1:
		test_otp()
	elif int(choice) == 2:
		get_public_key()
	elif int(choice) == 3:
		get_flag()
	else:
		print "Bye!"
		sys.exit(0)
