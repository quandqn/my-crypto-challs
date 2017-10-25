from Crypto.Util.number import *
import random
from flag import FLAG

def byte_to_binary(st):
	b = []
	for char in st:
		b+= [int(bit) for bit in list(bin(ord(char))[2:].zfill(8))]
	return b

def sequence(n):
	r = [random.randint(1, 2*n)]
	for i in range(1, n):
		r.append(random.randint(2 * r[i-1], 4 * r[i-1]))
	return r

def generate(n):
	r = sequence(n)
	B = random.randint(4 * r[-1], 8 * r[-1])
	A = random.randint(1, B)
	while not GCD(A, B) != 1:
		A = random.randint(1, B)
	M = [A * ri % B for ri in r]
	open("pubkey.txt", "w").write(str(M))
	return M

def encrypt(msg, pubkey):
	ciphertext = 0
	for i in range(len(msg)):
		ciphertext+= msg[i] * pubkey[i]
	open("enc.txt", "w").write(str(ciphertext))
	return ciphertext

FLAG = byte_to_binary(FLAG)
encrypt(FLAG, generate(len(FLAG)))

#Submit your flag as `MeePwnCTF{` + FLAG + `}`