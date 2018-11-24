#! /usr/bin/python3

from Midori64_perso import midori, antiMidori
from Sha3_perso import keccak
import trad


def padding(hexa):
	"""Fonction de padding. Le padding choisi ajoute en binaire 10*1 au message."""
	res = hexa
	if len(res)%16 == 15:
		res += '9' #1001
	else :
		res += '8' + '0'*(16 - (len(res)%16+2)) + '1' #1000 + 0000* + 0001
	return res


def unPadding(hexa):
	"""Fonction inverse du padding. On retire l'ensemble 10*1 en fin du message pour retrouver le message de base."""
	res = hexa
	if res[-1] == '9':
		res = res[:-1]
	else :
		res = res[:-1]
		while(res[-1] != '8'):
			res = res[:-1]
		res = res[:-1]
	return res


def decoupe(hexa):
	"""Découpage du message en hexadécimal vers un tableau d'hexa de bonne taille."""
	res = [hexa[16*i : 16*(i+1)] for i in range(len(hexa)//16)]
	return res


def convert(nb):
	"""Conversion d'un nombre quelconque en un nombre sur 32 bits. Cette fonction sert lors de la mise en forme du nonce ainsi que du compteur."""
	res = hex(nb)[2:]
	l = len(res)
	if l < 8:
		res = '0'*(8-l) + res
	return res[:8]


def CTR(nonce, hexa, key):
	"""Fonction de chiffrement basé sur l'utilisation du chiffremnt par bloc Midori en mode CTR."""
	res = ''
	ctr = 0
	M = decoupe(hexa)
	strNonce = convert(nonce)
	for Mi in M:
		strCtr = convert(ctr)
		strInput = strNonce + strCtr
		Input = [int(strInput[i], 16) for i in range(16)]
		tmp = midori(Input, key)
		Ci = ''
		for j in range(16):
			Ci += hex(tmp[j] ^ int(Mi[j], 16))[2:]
		res += Ci
	return res


if __name__ == '__main__' :
	nonce = 123456789
	key = [0 for i in range(32)]
	message = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ\0'
	hexa = trad.strToHex(message)
	hexa = padding(hexa)
	
	tmp = CTR(nonce, hexa, key)
	print("Message après chiffrement (Midori - CTR) :", tmp)
	tmp2 = CTR(nonce, tmp, key)
	tmp2 = unPadding(tmp2)
	print("Message après déchiffrement (Midori - CTR) :", tmp2)
	print("Traduction inverse du déchiffrement :", trad.hexToStr(tmp2))
	
