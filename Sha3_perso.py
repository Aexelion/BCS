#! /usr/bin/python3

##Sha3-512 : r = 512; c = 1024
##Sha3-384 : r = 832; c = 768
##Sha3-384 : r = 1088; c = 512
##Sha3-384 : r = 1152; c = 448


def padding(M,r):
	"""Ajoute du padding a un message quelconque afin de le rendre de taille multiple de r"""
	val = len(M + '11') % r
	res = M + '1' + '0'*((r-val)%r) + '1'
	return res


def toBlock(M, r):
	"""Transforme un message de taille multiple de r en un tableau de partie de message tous de taille r"""
	k = len(M) // r
	m = [M[r*i:(r+1)*i] for i in range(k)]
	return m


def createInit(tailleBlock=1600):
	"""Creer un block de taille tailleBlock (1600 par defaut) bits"""
	return '0'*tailleBlock


def xor(block, m, r):
	"""Realise un xor bit a bit entre un block de taille > r et un message de taille r"""
	res = [block[i] for i in range(len(block))]
	for i in range(r):
		res[i] = str(int(block[i])^int(m[i]))
	return res


def transformation(block):
	"""Transforme un block de 1600 bits en une matrice 3 dimension 5*5*64"""
	res = [['0'*64 for i in range(5)] for i in range(5)]
	for ligne in range(5):
		for colonne in range(5):
			res[ligne][colonne] = block[ligne*320+colonne*64:
			64+ligne*320+colonne*64]
	return res


def cp(matrice, x, z):
	"""Calcul de la parité de la colonne situé à l'emplacement x, z"""
	
	res = str(
	int(matrice[x][0][z]) ^
	int(matrice[x][1][z]) ^
	int(matrice[x][2][z]) ^
	int(matrice[x][3][z]) ^
	int(matrice[x][4][z])
	)
	return res


def theta(matrice):
	"""Fonction theta de Keccak realisé sur une matrice de 1600 bits decouper en matrice 5*5*64"""
	res = [['0'*64 for i in range(5)] for i in range(5)]
	for x in range(5):
		for y in range(5):
			for z in range(64):
				res[x][y] = res[x][y][:z] + \
				str(
				int(matrice[x][y][z]) ^
				int(cp(matrice, (x+1)%5, (z-1)%64)) ^
				int(cp(matrice, (x-1)%5, z))
				) + \
				res[x][y][(z+1):]
	return res


def f(block):
	"""Fonction de permutation de Keccak"""
	pass

if __name__ == "__main__" :
	init = '1'+'0'*1599
	mat = transformation(init)
	print(cp(mat, 0, 0)) 
	print(theta(mat))




