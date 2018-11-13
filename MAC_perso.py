#! /usr/bin/python3

from Midori64_perso import midori
import trad


def decoupe(hexa):
	pad = False
	if len(hexa)%16 != 0 :
		hexa += '8' + '0'*(16-(len(hexa)+1)%16)
		pad = True
	res = [hexa[16*i : 16*(i+1)] for i in range(len(hexa)//16)]
	return res, pad


def lastBlock(block, key, pad):
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
