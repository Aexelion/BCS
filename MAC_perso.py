#! /usr/bin/python3

from Midori64_perso import midori
import trad


def decoupe(hexa):
	if len(hexa)%16 != 0 :
		hexa += '0'*(16-len(hexa)%16)
	res = [hexa[16*i : 16*(i+1)] for i in range(len(hexa)//16)]
	return res


def CMAC(hexa, key1, key2):
	M = decoupe(hexa)
	res = '0'*16
	for Mi in M:
		Input = [int(Mi[i], 16) ^ int(res[i], 16) for i in range(16)]
		tmp = midori(Input, key1)
		res = ''
		for i in tmp:
			res += hex(i)[2:]
	tmp = ''
	for i in range(16):
		tmp += hex(int(res[i], 16) ^ key2[i])[2:]
	Input = [int(tmp[i], 16) for i in range(16)]
	tmp = midori(Input, key1)
	res = ''
	for i in tmp:
		res += hex(i)[2:]
	return res



if __name__ == '__main__' :
	key = [0 for i in range(32)]
	message = 'abcdefghijklmnopqrstuvwxz0123456789ABCDEFGHIJKLMNOPQRSTUVWXZ'
	hexa = trad.strToHex(message)
	mac = CMAC(hexa, key, key)
	print("MAC du message :", mac)
