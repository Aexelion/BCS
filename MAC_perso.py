#! /usr/bin/python3

from Midori64_perso import midori
import trad


def decoupe(hexa):
	"""Fonction permettant de découper un message (en hexa) en message de taille 16 pour préparer l'entrée du chiffrement Midori.
	Return le message découper ainsi qu'un booléen permettant de savoir si oui ou non le message à reçu du padding."""
	pad = False
	if len(hexa)%16 != 0 :
		hexa += '8' + '0'*(16-(len(hexa)%16+2)) + '1' #Padding utilisé : 1000 + 0000*
		pad = True
	res = [hexa[16*i : 16*(i+1)] for i in range(len(hexa)//16)]
	return res, pad


def lastBlock(block, key, pad):
	"""Modification du dernier bloc en utilisant le principe de OMAC."""
	input0 = [0 for i in range(16)]
	k0 = midori(input0, key)
	k1 = [k0[i] for i in range(15)]
	k1.append(0)
	if k0[0] >= 8 :
		k1[14] = k1[14] ^ 0x1
		k1[15] = k1[15] ^ 0xB
	k2 = [k1[i] for i in range(15)]
	k2.append(0)
	if k1[0] >= 8 :
		k2[14] = k2[14] ^ 0x1
		k2[15] = k2[15] ^ 0xB
	tmp = [int(block[i],16) for i in range(16)]
	res = ''
	if pad :
		for i in range(16):
			res += hex(tmp[i] ^ k2[i])[2:]
	else :
		for i in range(16):
			res += hex(tmp[i] ^ k1[i])[2:]
	return res


def CMAC(hexa, key):
	"""Fonction de calcul du MAC, en utilisant la méthode One-Key MAC (OMAC)."""
	M, pad = decoupe(hexa)
	res = '0'*16
	M[-1] = lastBlock(M[-1], key, pad)
	for Mi in M:
		Input = [int(Mi[i], 16) ^ int(res[i], 16) for i in range(16)]
		tmp = midori(Input, key)
		res = ''
		for i in tmp:
			res += hex(i)[2:]
	return res



if __name__ == '__main__' :
	key = [0 for i in range(32)]
	message = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	hexa = trad.strToHex(message)
	mac = CMAC(hexa, key)
	print("MAC du message :", mac)
