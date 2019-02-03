# Entity class player, embodies one of the players

from game.game.entityclass import entitydrawable
from game.game.map.mapmanager import MapManager as mam
from game.inputs.inputmanager import InputManager as im

import  math


class Player(entitydrawable.EntityDrawable):
	SPEED_ADD = 0.02
	SPEED_MAX = 0.09
	SPEED_DECREASE = 0.025

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.7, 0.4], True)
		self.entityRenderer.setImagePath([0.8, 1.2], "perso.png", [0.4, 0.2])

		self.attributes["collision"] = 1
		self.attributes["damage"] = 2
		self.attributes["heavy"] = 1
		self.attributes["interaction"] = 1
		self.attributes["door"] = 1

	def update(self):
		dir = [0, 0]
		if im.input(im.GO_LEFT):
			dir[0] -=1
		if im.input(im.GO_UP):
			dir[1] += 1
		if im.input(im.GO_RIGHT):
			dir[0] += 1
		if im.input(im.GO_DOWN):
			dir[1] -= 1

		for i in range(0,2):
			if dir[i] == 0:
				if self.speed[i] < 0:
					self.speed[i] += Player.SPEED_DECREASE
					if self.speed[i] > 0:
						self.speed[i] = 0
						self.inMov[i] = False
				else:
					self.speed[i] -= Player.SPEED_DECREASE
					if self.speed[i] < 0:
						self.speed[i] = 0
						self.inMov[i] = False
			else:
				self.inMov[i] = True
				self.speed[i] += dir[i] * Player.SPEED_ADD
				if math.fabs(self.speed[i]) > Player.SPEED_MAX:
					self.speed[i] = dir[i] * Player.SPEED_MAX

		if not self.speed[0] == 0:
			self.setPos([mam.checkCollisionX(self.pos, self.speed[0], self.halfColSize),
				self.pos[1]])
		if not self.speed[1] == 0:
			self.setPos([self.pos[0],
				mam.checkCollisionY(self.pos, self.speed[1], self.halfColSize)])
