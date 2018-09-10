#!/usr/bin/python2
import sys
import os
from Crypto.Util.number import *
import gmpy2
from Crypto.PublicKey import RSA
import random

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

flag = 'R0s3S-4r3-rED, v10l3ts-are-BLUE, 5ug@r-1s-sw33t, AnD...-s0-@r3-Y0u!'
welcome = 'Welcome to Rose and Sugar Area!\nLet\'s play with numbers!'
template = 'If N = {0}; e = {1} and c = {2}, so what is the message?'

print welcome

print '----- STAGE 1 -----'
rsa = RSA.generate(1024)
e = 3
stage = os.urandom(6).encode('hex')
print template.format(rsa.n, e, bytes_to_long(RSA.construct((long(rsa.n), long(e))).encrypt(stage, 0)[0]))
answer = raw_input('Send me the answer!\n>>> ')

if answer != stage:
	print 'Bye!'
	sys.exit(0)

print '----- STAGE 2 -----'
rsa = RSA.generate(1024)
phi = (rsa.p - 1) * (rsa.q - 1)
d_ = False
while not d_:
	d = random.getrandbits(256)
	if GCD(d, phi) == 1 and (36 * pow(d, 4) < rsa.n):
		d_ = True
e = gmpy2.invert(d, phi)
stage = os.urandom(16).encode('hex')
print template.format(rsa.n, e, bytes_to_long(RSA.construct((long(rsa.n), long(e))).encrypt(stage, 0)[0]))
answer = raw_input('Send me the answer!\n>>> ')

if answer != stage:
	print 'Bye!'
	sys.exit(0)

print '----- STAGE 3 -----'
n = 66257403459218493539989346665693974698231575577603976617927323957064847040727575710038994944717388281746981262596653093027480173702272209933896171854003810848614552660169975745658464035297649079910756473555323793826421980301473423824904391154746212588649369761555711202670869243820712726177249885744413201681L
e = 69
stage = os.urandom(16).encode('hex')
print template.format(n, e, bytes_to_long(RSA.construct((long(n), long(e))).encrypt(stage, 0)[0]))
answer = raw_input('Send me the answer!\n>>> ')

if answer != stage:
	print 'Bye!'
	sys.exit(0)

print '----- STAGE 4 -----'
rsa = RSA.generate(1024)
n = rsa.p * 31337
stage = os.urandom(16).encode('hex')
print template.format(n, rsa.e, bytes_to_long(RSA.construct((long(n), long(rsa.e))).encrypt(stage, 0)[0]))
answer = raw_input('Send me the answer!\n>>> ')

if answer != stage:
	print 'Bye!'
	sys.exit(0)

print '----- STAGE 5 -----'
rsa = RSA.generate(1024)
g = rsa.d * (rsa.p - 0xabadc0de)
stage = os.urandom(16).encode('hex')
print 'g = d * (p - 0xabadc0de) = {0}'.format(g)
print template.format(rsa.n, rsa.e, bytes_to_long(rsa.encrypt(stage, 0)[0]))
answer = raw_input('Send me the answer!\n>>> ')

if answer != stage:
	print 'Bye!'
	sys.exit(0)

print 'Well done, here is your reward!'
print flag
sys.exit(0)
