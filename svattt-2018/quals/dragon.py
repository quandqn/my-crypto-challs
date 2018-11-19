#!/usr/bin/python2
# -*- coding: utf-8 -*-	
import sys
import os
#from Crypto import Random
#from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.Util.number import *
from Crypto.Hash import SHA

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
FLAG = 'FLAG{Shenron doesn\'t like same k, so does ElGamal}'
"""
key = ElGamal.generate(1024, Random.new().read)
h = SHA.new(msg).digest()
while 1:
	k = random.StrongRandom().randint(1, key.p - 1)
	if GCD(k, key.p - 1) == 1: 
		break
print k
print [key.p, key.g, key.y, key.x]

# key generator, time-consuming...
# if you want to use your own parameters, make sure that
# gmpy2.invert(r, p-1) and gmpy2.invert(s1-s2, p-1)
# I recommend that using my parameters, tested.
"""
k = 889551647111842491997489376880381973454585634021952643143810214846415195789037662636090275206142898725217157947708986063107015035350839221129137597894265681610018445389340692711061642410893639249979198207288733400462450387899113
tup = (129395855808705212728342121899564040533627536165407217623699982163034898985604990453612738681235265684964910273382421570674875235106037524148312004154122323500944367988234700927644310658336581857679208804861661335768169851589929150626616698506529354785376916490328643358410300092039405295348822918174724269387L, 125119881720420900707670154269953309690838537679536446473408150363676013315875914220318853661265626997530402259420104771257078966641464155686445398996594055909718103795617751840611152747280651424068043671714408414771552296848509963265865300590662320297995606313265875459093865996548994154719802981360764938058L, 110720437718139700873489765502549555128025157595594830578305975049460354619156495297217470261777184549938149693476889162756827892972026584911305466259604054182286969266710088366635915899661932010493124108831364610393812629017634705994902225960644164776527794298493402388817192877039564691308012164937869143158L, 12841053699073275911948582609582036268035816999075891383482120347559247896616288846996721466728842982835660588351096284144328709549322351938920824008376895019700428848240004524021310165326109738573794348659829181144052586134072911352831288002506748789000912905006051038498110861831292263097809911298247559460L)
key = ElGamal.construct(tup)

menu = """----- 🐉 Dragon Ball Verification System 🐉 -----
1. ?generate
2. ?verify
3. ?debug
>>> """

def genToken(username):
	cred = 'USERNAME={0}&LEVEL={1}'.format(username, 'Saiyan')
	h = SHA.new(str(cred)).digest()
	r, s = key.sign(h, k)
	return (cred + '&r=' + long_to_bytes(r) + '&s=' + long_to_bytes(s)).encode('base64')

def verifyToken(token):
	try: 
		token = token.decode('base64')
		cred = token.split('&r=')[0]
		(r, s) = (bytes_to_long(token.split('&r=')[1].split('&s=')[0]), bytes_to_long(token.split('&r=')[1].split('&s=')[1]))
		if key.verify(SHA.new(cred).digest(), (r, s)):
			level = cred.split('&LEVEL=')
			username, level = level[0].split('USERNAME=')[1], level[-1]
			if level == 'SuperSaiyan':
				return 'Hooooo! Shenron will give you the FLAG!\n' + FLAG
			else:
				return 'Sorry {0}, on this planet, only SuperSaiyan can summon Shenron! Transform and try again!'.format(username)
		else:
			return 'Verification failed. Try again!'
	except:
		return 'Verification failed. Try again!'

while 1:
	choice = raw_input(menu)
	try: 
		choice = int(choice)
	except:
		print 'Bye!'
		sys.exit(0)
	if int(choice) == 1:
		name = raw_input('Your name: ')
		print 'Hi {0}, your LEVEL is Saiyan.\n'.format(name)
		print 'Say', genToken(name).replace('\n', ''), 'to summon Shenron!'
	elif int(choice) == 2:
		token = raw_input('Summon Shenron: ')
		print verifyToken(token)
		sys.exit(0)
	elif int(choice) == 3:
		print """----- DEBUG MODE -----
	# We used ElGamal signature scheme with 
	>>> p = {0}
	>>> g = {1}
	# SHA is the Hash Function we used.
	>>> h = SHA.new('USERNAME=username&LEVEL=Saiyan').digest()
	# Example: 
	# (from https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.ElGamal-module.html)
	>>> from Crypto import Random
	>>> from Crypto.Random import random
	>>> from Crypto.PublicKey import ElGamal
	>>> from Crypto.Util.number import GCD
	>>> from Crypto.Hash import SHA
	>>>
	>>> message = "Hello"
	>>> key = ElGamal.generate(1024, Random.new().read)
	>>> h = SHA.new(message).digest()
	>>> while 1:
	>>>     k = random.StrongRandom().randint(1,key.p-1)
	>>>     if GCD(k,key.p-1)==1: break
	>>> sig = key.sign(h,k)
	>>> ...
	>>> if key.verify(h,sig):
	>>>     print "OK"
	>>> else:
	>>>     print "Incorrect signature"
	""".format(key.p, key.g)
	else:
		print 'Bye!'
		sys.exit(0)
