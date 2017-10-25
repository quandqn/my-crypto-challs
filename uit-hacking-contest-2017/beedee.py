import gmpy2
import hashlib
from Crypto.Util.number import *
from Crypto.PublicKey import RSA

y = 120665291705719690115222322113716317407319531890879466832310307659286695337787574333320572934753119956332198188966236998063469953794256479776940706801779722984334459553487739933982153230430931061694713280415545780277794282413523090700138281599496145125950496926462172253328559156755158737383824919762030663757
#Trust me, this is a random 1024-bit integer, so strong!
e = (1 << 16) + 1 #super secure public exponent
flag = open("flag").read()

def concat(a, b):
	return bytes_to_long(long_to_bytes(a) + long_to_bytes(b))
	
n = 0
while gmpy2.mpz(n).bit_length() != 2048: #2048-bit integer, no one can factorize it! 
	while 1:
		s = getRandomNBitInteger(1024) #random 1024-bit, truly random, haha
		p = bytes_to_long(hashlib.sha512(str(s)).digest()) #sha512 is safe enough, right?
		if isPrime(p):
			break

	while 1:
		rnd = getRandomNBitInteger(1024) #another truly 1024-bit random, more noise 
		c = gmpy2.powmod(s, e, y)
		q, r = divmod(concat(c, rnd), p)
		if isPrime(q):
			break
	n = p * q

m = bytes_to_long(flag)
c = pow(m, e, n)
open("flag.encrypted", "w").write("{0}: {1}: {2}".format(n, e, c))
