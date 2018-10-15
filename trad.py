#! /usr/bin/python3


def strToHex(s):
	res = ''
	for i in s:
		res += hex(ord(i))[2:]
	return res


def hexToStr(h):
	res = ''
	for i in range(0, len(h), 2) :
		res += chr(int(h[i:i+2], 16))
	return res


def strToBin(s):
	res = ''
	for i in s:
		tmp = bin(ord(i))[2:]
		res += '0'*(8-len(tmp)) + tmp
	return res


def binToStr(b):
	res = ''
	for i in range(0, len(b), 8):
		res += chr(int(b[i:i+8], 2))
	return res



if __name__ == '__main__' :
	test = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
	print(test)
	
	print('\n--- Test sur la traduction en hexadecimal ---\n')
	hexa = strToHex(test)
	print(hexa)
	testFromHexa = hexToStr(hexa)
	print(testFromHexa)
	
	print('\n--- Test sur la traduction en binaire ---\n')
	binaire = strToBin(test)
	print(binaire)
	testFromBin = binToStr(binaire)
	print(testFromBin)
