def AND(a: [bool, int], b: [bool, int]):
	if a and b:
		return True
	return False


def OR(a: [bool, int], b: [bool, int]):
	if a or b:
		return True
	return False


def XOR(a: [bool, int], b: [bool, int]):
	return bool(a ^ b)


def NOT(a: [bool, int]):
	return not a


def NAND(a: [bool, int], b: [bool, int]):
	if NOT(a) and NOT(b):
		return True
	return False


def NOR(a: [bool, int], b: [bool, int]):
	if NOT(OR(a, b)):
		return True
	return False


def XNOR(a: [bool, int], b: [bool, int]):
	return NOT(XOR(a, b))


def EXNOR(a: [bool, int], b: [bool, int]):
	return NOT(XOR(a, b))


def EXOR(a: [bool, int], b: [bool, int]):
	return NOT(EXNOR(a, b))


def RANDOM(seed_=54574458):
	from random import randint, seed
	seed(seed_)
	return bool(randint(0, 1))
