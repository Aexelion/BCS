#! /usr/bin/python3

from MAC_perso import CMAC
from ModeOp import CTR
from Sha3_perso import keccak
import trad
import argparse
import sys
from getpass import getpass


def Encrypt_Then_MAC(message, mdp):
	hexa = trad.strToHex(message)
	mdpBin = trad.strToBin(mdp)
	tmp = keccak(mdpBin, 512)
	nonce = int(tmp[-32:], 2)
	keyCTR = [int(tmp[4*i:4*i+4], 2) for i in range(32)]
	keyMAC = [int(tmp[128+4*i:128+4*i+4], 2) for i in range(32)]
	res = CTR(nonce, hexa, keyCTR)
	res += CMAC(res, keyMAC)
	return res


def Check_Then_Decrypt(hexa, mdp):
	res = ''
	mdpBin = trad.strToBin(mdp)
	tmp = keccak(mdpBin, 512)
	nonce = int(tmp[-32:], 2)
	keyCTR = [int(tmp[4*i:4*i+4], 2) for i in range(32)]
	keyMAC = [int(tmp[128+4*i:128+4*i+4], 2) for i in range(32)]
	if CMAC(hexa[:-16], keyMAC) == hexa[-16:]:
		res = CTR(nonce, hexa[:-16], keyCTR)
		res = trad.hexToStr(res)
	else :
		res = 'vérification du MAC non valide'
	return res


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
	description='Chiffre/Déchiffre un message avec un mot de passe spécifié.',
	epilog='Si aucune option n\'est spécifié, seul l\'option \'-e\' est prise en compte.'
	)
	parser.add_argument('-e', '--encrypt', 
	action='store_true', 
	help="Specifie que l'on souhaite chiffrer le message."
	)
	parser.add_argument('-d', '--decrypt', 
	action='store_true', 
	help='Permet de choisir de dechiffrer le message.'
	)
	parser.add_argument('-p', '--password',
	action='store_true',
	help='Permet de taper le mot de passe sans affichage.'
	)
	parser.add_argument('-o', '--output',
	metavar='File', 
	type=argparse.FileType('w'),
	default=sys.stdout,
	help='Specifie un fichier de sortie.'
	)
	parser.add_argument('-i', '--input', 
	metavar='File',
	type=argparse.FileType('r'),
	default=sys.stdin,
	help='Spécifie un fichier d\'entrée.'
	)
	
	args = parser.parse_args()
	
	if args.decrypt and args.encrypt:
		sys.stderr.write('Un seul choix possible pour chiffrement ou déchiffrement.\n')
		parser.print_help()
		exit(1)
	
	text = ''
	mdp = ''
	if args.decrypt:
		if '<stdin>' == args.input.name:
			text = input("Entrer le message à déchiffrer :\n")
		else:
			text = args.input.read()
	else :
		if '<stdin>' == args.input.name:
			text = input("Entrer le message à chiffrer :\n")
		else :
			text = args.input.read()
	if args.password:
		mdp = getpass("Entrer votre mot de passe : ")
	else:
		mdp = input("Entrer votre mot de passe : ")
	
	res = ''
	if args.decrypt:
		res = Check_Then_Decrypt(text, mdp)
		res = res.strip()
	else:
		res = Encrypt_Then_MAC(text, mdp)
	
	if '<stdout>' == args.output.name:
		print(res)
	else:
		args.output.write(res)
	
	
	
	
	
	
	
	
	
	
	
	
	
