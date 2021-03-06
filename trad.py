#! /usr/bin/python3


def strToHex(s):
	"""Fonction de traduction d'une chaîne de caractère vers une chaîne en hexadécimal."""
	res = ''
	for i in s:
		tmp = hex(ord(i))[2:]
		res += '0'*(len(tmp)%2) + tmp
	return res


def hexToStr(h):
	"""Fonction de traduction d'une chaîne en hexadécimal vers une chaîne de caractère."""
	res = ''
	for i in range(0, len(h), 2) :
		res += chr(int(h[i:i+2], 16))
	return res


def strToBin(s):
	"""Fonction de traduction d'une chaîne de caractère vers une chaîne en binaire."""
	res = ''
	for i in s:
		tmp = bin(ord(i))[2:]
		res += '0'*(8-len(tmp)) + tmp
	return res


def binToStr(b):
	"""Fonction de traduction d'une chaîne en binaire vers une chaîne de caractère."""
	res = ''
	for i in range(0, len(b), 8):
		res += chr(int(b[i:i+8], 2))
	return res


def binToHex(b):
	"""Fonction de traduction d'une chaîne en binaire vers une chaîne en hexadécimal."""
	res = ''
	for i in range(0, len(b), 8):
		res += hex(int(b[i:i+8], 2))[2:]
	return res


def hexToBin(h):
	"""Fonction de traduction d'une chaîne en hexadécimal vers une chaîne en binaire."""
	res = ''
	for i in range(0, len(h), 2) :
		res += bin(int(h[i:i+2], 16))[2:]
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
	print(binaire, '\n\n\n')
	testFromBin = binToStr(binaire)
	print(testFromBin)
