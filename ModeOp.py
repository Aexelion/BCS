#! /usr/bin/python3

from Midori64_perso import midori, antiMidori
from Sha3_perso import keccak
import trad


def decoupe(hexa):
	if len(hexa)%16 != 0 :
		hexa += '0'*(16-len(hexa)%16)
	res = [hexa[16*i : 16*(i+1)] for i in range(len(hexa)//16)]
	return res


def convert(nb):
	res = hex(nb)[2:]
	l = len(res)
	if l < 8:
		res = '0'*(8-l) + res
	return res[:8]


def CTR(nonce, hexa, key, mode=0):
	ctr = 0
	M = decoupe(hexa)
	C = []
	strNonce = convert(nonce)
	for Mi in M:
		strCtr = convert(ctr)
		strInput = strNonce + strCtr
		Input = [int(strInput[i], 16) for i in range(16)]
		tmp = midori(Input, key)
		Ci = ''
		for j in range(16):
			Ci += hex(tmp[j] ^ int(Mi[j], 16))[2:]
		C.append(Ci)
		ctr += 1
	res = ''
	for Ci in C:
		res += Ci
	return res


if __name__ == '__main__' :	
	nonce = 123456789
	key = [0 for i in range(32)]
	message = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	hexa = trad.strToHex(message)
	
	tmp = CTR(nonce, hexa, key, 0)
	print("Message après chiffrement (Midori - CTR) :", tmp)
	tmp2 = CTR(nonce, tmp, key, 1)
	print("Message après déchiffrement (Midori - CTR) :", tmp2)
	print("Traduction inverse du déchiffrement :", trad.hexToStr(tmp2))
	
