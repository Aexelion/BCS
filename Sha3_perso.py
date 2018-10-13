#! /usr/bin/python3


def padding(M,r):
	"""Ajoute du padding a un message quelconque afin de le rendre de taille multiple de r."""
	
	val = len(M + '11') % r
	res = M + '1' + '0'*((r-val)%r) + '1'
	return res


def toBlock(M, r):
	"""Transforme un message de taille multiple de r en un tableau de partie de message tous de taille r."""
	
	k = len(M) // r
	m = [M[r*i:r*(i+1)] for i in range(k)]
	return m


def xor(block, m, r):
	"""Realise un xor bit a bit entre un block de taille > r et un message de taille r."""
	
	res = [block[i] for i in range(len(block))]
	for i in range(r):
		res[i] = str(int(block[i])^int(m[i]))
	return res


def transformation(block):
	"""Transforme un block de 1600 bits en une matrice 3 dimension 5*5*64."""
	
	res = [['0'*64 for i in range(5)] for i in range(5)]
	for ligne in range(5):
		for colonne in range(5):
			res[ligne][colonne] = block[ligne*320+colonne*64 :
			64+ligne*320+colonne*64]
	return res


def detransformation(matrice):
	"""Transforme une matrice 3 dimension 5*5*64 en un block de 1600 bits."""
	
	res = ''
	for ligne in range(5):
		for colonne in range(5):
			res += matrice[ligne][colonne]
	return res


def cp(matrice, x, z):
	"""Calcul de la parité de la colonne situé à l'emplacement x, z."""
	
	res = str(
	int(matrice[x][0][z]) ^
	int(matrice[x][1][z]) ^
	int(matrice[x][2][z]) ^
	int(matrice[x][3][z]) ^
	int(matrice[x][4][z])
	)
	return res


def theta(matrice):
	"""Fonction theta de Keccak realisé sur une matrice de 1600 bits découpé en matrice 5*5*64. Réalisation d'un ensemble de xor sur les différents bits de la matrice."""
	
	res = [['0'*64 for i in range(5)] for i in range(5)]
	for x in range(5):
		for y in range(5):
			for z in range(64):
				res[x][y] = res[x][y][:z] + \
				str(
				int(matrice[x][y][z]) ^
				int(cp(matrice, (x+1)%5, (z-1)%64)) ^
				int(cp(matrice, (x-1)%5, z))
				)
	return res


def rho(matrice):
	"""Fonction rho de Keccak réalisé sur une matrice de 1600 bits découpée en matrice 5*5*64. Réalisation d'un ensemble de rotation sur les mots de 64 bits dans la matrice 5*5."""
	
	rotation = [[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
	res = [['0'*64 for i in range(5)] for i in range(5)]
	for x in range(5):
		for y in range(5):
			res[x][y] = matrice[x][y][rotation[x][y]:] + matrice[x][y][:rotation[x][y]]
	return res


def pi(matrice):
	"""Fonction pi de Keccak réalisé sur une matrice de 1600 bits découpée en matrice 5*5*64. Réalisation d'un mélange des mots de 64 bits dans la matrice 5*5."""
	
	res = [['0'*64 for i in range(5)] for i in range(5)]
	for x in range(5):
		for y in range(5):
			res[x][y] = matrice[y][(2*x+3*y)%5]
	return res


def khi(matrice):
	"""Fonction khi de Keccak réalisé sur une matrice de 1600 bits découpée en matrice 5*5*64. Réalisation d'un ensemble d'opération sur les différents bits de la matrice."""
	
	res = [['0'*64 for i in range(5)] for i in range(5)]
	for x in range(5):
		for y in range(5):
			for z in range(64):
				res[x][y] = res[x][y][:z] + \
				str(
				int(matrice[x][y][z]) ^
				((int(matrice[(x+1)%5][y][z]) ^ 1) &
				int(matrice[(x+2)%5][y][z]))
				)
	return res


def hexToBin(hexa):
	"""Transforme un nombre en hexadecimal en un mot de 64 bits."""
	
	res = bin(hexa)[2:]
	res = '0'*(64-len(res))+res
	return res


def iota(matrice, roundNb):
	"""Fonction iota de Keccak réalisé sur une matrice de 1600 bits découpée en matrice 5*5*64. Ajout d'une constante sur la 1ere ligne de la matrice 5*5 (située en 0,0)."""
	
	RC = [
	0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
	0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
	0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
	0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
	0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
	0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
	0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
	0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
	
	binRC = hexToBin(RC[roundNb])
	
	res = [[matrice[j][i] for i in range(5)] for j in range(5)]
	for z in range(64):
		res[0][0] = res[0][0][:z] + \
		str(
		int(matrice[0][0][z]) ^
		int(binRC[z])
		)
	return res


def f(block):
	"""Fonction de permutation de Keccak."""
	matrice = transformation(block)
	for i in range(24):
		matrice = theta(matrice)
		matrice = rho(matrice)
		matrice = pi(matrice)
		matrice = khi(matrice)
		matrice = iota(matrice, i)
	res = detransformation(matrice)
	return res


##Sha3-512 : r = 576; c = 1024
##Sha3-384 : r = 832; c = 768
##Sha3-256 : r = 1088; c = 512
##Sha3-224 : r = 1152; c = 448

def keccak(M, version):
	v = {512:576, 384:832, 256:1088, 224:1152}
	if (not version in v):
		print('Version non valide pour Keccak.')
		exit(1)
	else :
		r = v[version]
		c = 1600-r
	
	tmp = padding(M, r)
	ensMessage = toBlock(tmp, r)
	block = '0'*1600
	
	for m in ensMessage:
		block = xor(block, m, r)
		block = f(block)
	
	res = block[:version]
	return res


if __name__ == "__main__" :
	res = keccak('0110', 512)
	print("miaou")



