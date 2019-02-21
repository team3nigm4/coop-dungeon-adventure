# Entity class player, embodies one of the players

import math

from game.game.entityclass import entitycomplex

class Player(entitycomplex.EntityComplex):
	SPEED_ADD = 0.015
	SPEED_MAX = 0.09
	SPEED_DECREASE = 0.025

	ARGS_PLAYER_NUMBER = 2
	ARGS_PLAYER_TEXTURE = 3

	INVINCIBILITY_TIME = 60

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.6, 0.4], True)
		self.playerNumber = args[Player.ARGS_PLAYER_NUMBER]

		self.attributes["collision"] = 1
		self.attributes["enemyDamage"] = 2
		self.attributes["heavy"] = 1
		self.attributes["door"] = 1

		self.wantDirection = [0, 0]
		self.direction = 3
		self.damage = 1
		self.life = 6
		self.maxSpeed = Player.SPEED_MAX
		self.invincibilityTime = Player.INVINCIBILITY_TIME

		from game.game.gameplay import itemweapon
		self.item = itemweapon.ItemWeapon(self)

		self.setDrawCol(True)
		self.colRenderer.setAttributes(self.colSize, [0, 1, 0, 1])

		self.entityRenderer.setImagePath([1, 1.5], args[Player.ARGS_PLAYER_TEXTURE], [0.45, 0.2])

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
		self.item.update()

		if (self.wantDirection[0] != 0 and self.wantDirection[1] == 0) or (
				self.wantDirection[1] != 0 and self.wantDirection[0] == 0):
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
				if math.fabs(self.speed[i]) > self.maxSpeed:
					self.speed[i] = self.wantDirection[i] * self.maxSpeed

		if not self.speed[0] == 0:
			self.mam.checkCollisionX(self)
		if not self.speed[1] == 0:
			self.mam.checkCollisionY(self)
		self.wantDirection = [0, 0]

		self.mam.checkEmpty(self)

	def setLife(self, newLife, death=False):
		super().setLife(newLife, death)

	def applyDamage(self, damage, death=False):
		if self.life == 0:
			if self.em.entities[1 - self.playerNumber].life > 0:
				self.em.entities[1 - self.playerNumber].applyDamage(damage)
			else:
				print("Two players are dead !!")
				exit()
		else:
			super().applyDamage(damage, death)
			if self.life <= 0:
				self.life = 0
				if self.em.entities[1 - self.playerNumber].life <= 0:
					print("Two players are dead !!")
					exit()

	def collision(self, ent):
		if ent.attributes["enemyDamage"] == 1:
			self.applyDamage(ent.damage)

		super().collision(ent)
