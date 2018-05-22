#!/usr/bin/python
import os
import sys
from hashlib import sha1, md5
from Crypto.Cipher import DES
from base64 import b64encode, b64decode

SECRET = os.urandom(16)

part1 = 'flag{hash_length_extension_attack_|'
part2 = '|_weak_keys_in_DES___a_chain_of_failure}'

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

pad = lambda s: (s + (8 - len(s) % 8) * chr(8 - len(s) % 8))[0:8]

_MENU = """
1. Register
2. Login
3. Quit"""

def _superencrypt(k, kk, kkk):
	kkkk = DES.new(k, DES.MODE_ECB)
	kkkkk = kkkk.encrypt(kkk)
	kkkkkk = DES.new(kk, DES.MODE_ECB)
	return kkkkkk.encrypt(kkkkk)

def generate_creds(uname, passwd):
	ROLE = '0'
	s = "uname={}&passwd={}&ROLE={}".format(uname, passwd.encode('hex'), ROLE)
	s+= "&sign=" + sha1(SECRET + s).hexdigest()
	return b64encode(s)

def register():
	uname = raw_input('Username: ')
	passwd = raw_input('Password: ')

	if uname and passwd:
		print 'You have successfully registered as {0}!'.format(uname)
		print 'Use this code to login:', generate_creds(uname, passwd)

def parse(info):
	block = info.split('&')
	for b in block:
		if b.startswith('ROLE='):
			ROLE = b[5:]
		if b.startswith('uname='):
			uname = b[6:]
		if b.startswith('passwd='):
			passwd = b[7:].decode('hex')
	return [uname, passwd, ROLE]

def login():
	creds = raw_input('Enter your creds: ')
	creds = b64decode(creds)
	creds = creds.split("&sign=")
	creds, sign = creds[0], creds[1]

	if sha1(SECRET + creds).hexdigest() == sign:
		uname, passwd, ROLE = parse(creds)
		print 'You have logged in successfully as {0}!'.format(uname)
		if ROLE == '0':
			print 'Hm... your ROLE is 0, no flag for you!'
			print 'Please upgrade your ROLE to 1 to view flag.'
		elif ROLE == '1':
			if uname == 'admin':
				print 'Welcome admin, HOWDY!'
				print 'This is your first part of flag:', part1
				print 'Please upgrade your ROLE to 2 to view the second part of flag.'
			else:
				print 'Only \'admin\' who has ROLE=1 can see this section.'
		elif ROLE == '2':
			while True:
				print '-----Hidden Area-----\n1. view-secret\n2. view-source\n3. Quit'
				_choice = raw_input('>>> ')

				if _choice == '1':
					key = raw_input('Input your 8 bytes key (hex-encoded) to see the secret: ').decode('hex')
					if md5(key).hexdigest() == md5(passwd).hexdigest():
						print 'For security purpose, your key is not allowed to be the same with your password!'
						print 'Bye!'
					else:
						try:
							if _superencrypt(pad(passwd), pad(key), uname) == 'iamgroot':
								print 'Hi gr00t, this is your 2nd part of flag:', part2
								print 'Bye!'
							else: 
								print 'Nope! Who are you?'
						except:
							print 'Invalid username/key length!'
				elif _choice == '2':
					print 'https://gist.github.com/quandqn/d637ecbae4abf3f675c2767445fd7da6'
				else:
					print 'Bye!'
					break
		else:
			print 'Invalid username/role!'
	else:
		print 'Invalid creds!'

print "-----ABCXYZ Admin Panel-----"
while True:
	print _MENU
	choice = raw_input(">>> ")
	if choice == '1':
		register()
	elif choice == '2':
		login()
	else:
		break
