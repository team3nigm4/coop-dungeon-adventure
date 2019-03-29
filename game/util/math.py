import math

def distP(pos1, pos2):
	return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def distPx(pos1, pos2):
	return math.sqrt((pos1 - pos2) ** 2)

def distPy(pos1, pos2):
	return math.sqrt((pos1 - pos2) ** 2)

def distOldE(ent1, ent2):
	return distP(ent1.oldPos, ent2.oldPos)

def distE(ent1, ent2):
	return distP(ent1.pos, ent2.pos)

def distEx(ent1, ent2):
	return distPx(ent1.pos[0], ent2.pos[0])

def distEy(ent1, ent2):
	return distPx(ent1.pos[1], ent2.pos[1])

def map(z, x, y, a, b):
	return (z - x) / (y - x) * (b - a) + a
