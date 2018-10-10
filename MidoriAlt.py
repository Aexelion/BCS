#!/usr/bin/python3

Sbox0 = [0xc, 0xa, 0xd, 0x3, 0xe, 0xb, 0xf, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]
#Sbox1 = [0x1, 0x0, 0x5, 0x3, 0xe, 0x2, 0xf, 0x7, 0xd, 0xa, 0x9, 0xb, 0xc, 0x8, 0x4, 0x6]




def subcells(s):
	res = 0;
	for i in range(16):
		res |= Sbox0[(s >> 4*i)& 0xf] << 4*i
	return res


def shuffleCell(s):
	p = [0,10,5,15,14,4,11,1,9,3,12,6,7,13,2,8]
	res = 0;
	for i in range (16):
		res |= ((s >> 4*p[i])& 0xf) << 4*i
	return res

def mixColumn(s):
	res = 0
	#MS=[0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0]
	for i in range(4):
		t = (s >> 16*i)&0xffff
		u = ((t >> 4) ^ (t >>8) ^ (t>>12))&0xf
		u |= ((t)^(t>>8)^(t>>12)&0xf)<<4
		u |= ((t)^(t>>8)^(t>>12)&0xf)<<8
		u |= ((t)^(t>>8)^(t>>12)&0xf)<<12
		res |= u <<16*i
	return res



def midori64(m,k):
	k=[k&0xffffffffffffffff,k>>64]
	wk=k[0]^k[1]
	#Définition de la matrice Alpha
	A0 =  0x0001010110110011
	A1 =  0x0111100011000000
	A2 =  0x1010010000110101
	A3 =  0x0110001000010011
	A4 =  0x0001000001001111
	A5 =  0x1101000101110000
	A6 =  0x0000001001100110
	A7 =  0x0000101111001100
	A8 =  0x1001010010000001
	A9 =  0x0100000010111000
	A10 = 0x0111000110010111
	A11 = 0x0010001010001110
	A12 = 0x0101000100110000
	A13 = 0x1111100011001010
	A14 = 0x1101111110010000
	A = [A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14]
	s= m ^ wk
	for i in range(15):
		s=subcells(s)
		s=shuffleCell(s)
		s=mixColumn(s)
		s ^= k[i%2] ^ A[i]
	s=subcells(s)
	return s^wk
	
if __name__ == '__main__':
	print(hex(midori64(0x0, 0x0)))
