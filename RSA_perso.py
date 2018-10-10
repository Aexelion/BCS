#!/usr/bin/python3

import random

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modInv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def expRapide(a, n, m):
	res = 1
	while n > 0:
		if n % 2 == 1:
			res = (res * a) % m
		a = (a * a) % m
		n = n // 2
	return res

#print(expRapide(10, 5, 100000))


def isPrime(nb):
	res = (expRapide(2, nb-1, nb) == 1) \
	and (expRapide(3, nb-1, nb) == 1) \
	and (expRapide(5, nb-1, nb) == 1) \
	and (expRapide(7, nb-1, nb) == 1)
	return res


def genPrime(size):
	res = random.getrandbits(size) | 0x1
	prime = isPrime(res)
	while not(prime):
		res += 2
		prime = isPrime(res)
	return res

#print(genPrime(1024))


def genCouple():
	p = genPrime(1024)
	q = genPrime(1024)
	while p == q :
		q = genPrime()
	return (p,q)

def genE(phiN):
	e=1
	while (phiN % e != 1):
		e+=1
	return e

def genD(e, phiN):
	return modInv(e, phiN)

def encryptRSA(m, e, N):
	return expRapide(m, e, N)
	
def decryptRSA(c, d, N):
	return expRapide(c, d, N)



if __name__ == "__main__":
	p, q = genCouple()
	N = p*q
	phiN = (p-1)*(q-1)
	e = genE(phiN)
	d = genD(e, phiN)
	
	message = 9876543210123456789
	chiffre = encryptRSA(message, e, N)
	dechiffre = decryptRSA(chiffre, d, N)
	
	print("p = {}\n".format(p))
	print("q = {}\n".format(q))
	print("e = {}\n".format(e))
	print("d = {}\n".format(d))
	print("message = {}\n".format(message))
	print("\n----- Partie calcul -----\n\n")
	print("chiffre = {}\n".format(chiffre))
	print("dechiffre = {}\n".format(dechiffre))
	
	
