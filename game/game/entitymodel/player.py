# Entity class player, embodies one of the players

from game.game.entityclass import entitycomplex
from game.game.map.mapmanager import MapManager as mam

import  math


class Player(entitycomplex.EntityComplex):
	SPEED_ADD = 0.015
	SPEED_MAX = 0.09
	SPEED_DECREASE = 0.025

	ARGS_PLAYER_NUMBER = 2
	ARGS_PLAYER_TEXTURE = 3

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.7, 0.4], True)
		self.playerNumber = args[Player.ARGS_PLAYER_NUMBER]

		self.entityRenderer.setImagePath([0.8, 1.2], args[Player.ARGS_PLAYER_TEXTURE], [0.4, 0.2])

		self.attributes["collision"] = 1
		self.attributes["damage"] = 2
		self.attributes["heavy"] = 1
		self.attributes["door"] = 1

		self.wantDirection = [0, 0]
		self.direction = 3
		from game.game.gameplay import itemkey
		self.item = itemkey.ItemKey(self)

	def left(self, input):
		if input > 1:
			self.wantDirection[0] -=1

	def up(self, input):
		if input > 1:
			self.wantDirection[1] +=1

	def right(self, input):
		if input > 1:
			self.wantDirection[0] +=1

	def down(self, input):
		if input > 1:
			self.wantDirection[1] -=1

	def useItem(self, input):
		if input == 2:
			self.item.useItem()

	def useItem2(self, input):
		if input == 2:
			self.item.useItem2()

	def interact(self, input):
		if input == 2:
			self.attributes["interaction"] = 1
		else:
			self.attributes["interaction"] = 0

	def update(self):
		super().update()

		if (self.wantDirection[0] != 0 and self.wantDirection[1] == 0) or (self.wantDirection[1] != 0 and self.wantDirection[0] == 0):
			if self.wantDirection[0] == -1:
				self.direction = 0
			elif self.wantDirection[1] == 1:
				self.direction = 1
			elif self.wantDirection[0] == 1:
				self.direction = 2
			else:
				self.direction = 3

		for i in range(2):
			if self.wantDirection[i] == 0:
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
				self.speed[i] += self.wantDirection[i] * Player.SPEED_ADD
				if math.fabs(self.speed[i]) > Player.SPEED_MAX:
					self.speed[i] = self.wantDirection[i] * Player.SPEED_MAX

		if not self.speed[0] == 0:
			mam.checkCollisionX(self)
		if not self.speed[1] == 0:
			mam.checkCollisionY(self)
		self.wantDirection = [0, 0]

		mam.checkEmpty(self)

	def triggerBox(self):
		self.item.used()
