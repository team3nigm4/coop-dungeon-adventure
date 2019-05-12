# Entity class player, embodies one of the players

import math
from sys import exit

from game.game.entityclass import entitycomplex

class Player(entitycomplex.EntityComplex):
	SPEED_ADD = 0.015
	SPEED_MAX = 0.09
	SPEED_DECREASE = 0.025

	ARGS_PLAYER_NUMBER = 3

	INVINCIBILITY_TIME = 90

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.65, 0.405])
		self.setCollision(True)
		self.playerNumber = args[Player.ARGS_PLAYER_NUMBER]

		self.attributes["collision"] = 1
		self.attributes["enemyDamage"] = 2
		self.attributes["heavy"] = 1
		self.attributes["door"] = 1
		self.attributes["blockDamage"] = 1

		self.wantDirection = [0, 0]
		self.direction = 3
		self.life = 6
		self.maxSpeed = Player.SPEED_MAX
		self.invincibilityTime = Player.INVINCIBILITY_TIME

		self.canInteract = False
		self.wantTexture = ""
		self.changeTexture = True

		self.weight = 1.3

		if self.playerNumber == 0:
			#self.setItem("Key")
			self.setItem("Weapon")
		else:
			self.setItem("Weapon")

		self.setDrawCol(True)
		self.colRenderer.setAttributes(self.colSize, [1, 1, 0, 0.5])

		self.setDisplayLayer(self.em.DISPLAY_MIDDLE)

	def useItem(self, input):
		if input == 2 and not self.stuned:
			self.item.useItem()

	def useItem2(self, input):
		if input == 2 and not self.stuned:
			self.item.useItem2()

	def interact(self, input):
		if input == 2 and not self.stuned:
			self.attributes["interaction"] = 1
		else:
			self.attributes["interaction"] = 0

	def update(self):
		super().update()
		self.item.update()

		# Change the direction choose by the player
		if (not self.wantDirection[0] == 0 and self.wantDirection[1] == 0) or (
				not self.wantDirection[1] == 0 and self.wantDirection[0] == 0) or (
				self.oldWantDirection == [0, 0]):
			# In priority up and down direction
			if self.wantDirection[1] == 1:
				self.setDirection(1)
			elif self.wantDirection[1] == -1:
				self.setDirection(3)
			elif self.wantDirection[0] == -1:
				self.setDirection(0)
			elif self.wantDirection[0] == 1:
				self.setDirection(2)

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

		if self.changeTexture:
			if self.wantTexture == "":
				self.entityRenderer.setImage([0.80, 2], "player-" + str(self.playerNumber + 1) + "-" + str(self.direction), [0.40, 0.625])
			else:
				if self.wantTexture == "sword":
					if self.direction == 0:
						self.entityRenderer.setImage([1.6, 2],
													 "player-" + str(self.playerNumber + 1) + "-" + str(self.direction) + "-" + self.wantTexture,
													 [1.2, 0.625])
					elif self.direction == 2:
						self.entityRenderer.setImage([1.6, 2],
													 "player-" + str(self.playerNumber + 1) + "-" + str(self.direction) + "-" +  self.wantTexture,
													 [0.4, 0.625])
					else:
						self.entityRenderer.setImage([0.80, 2],
													 "player-" + str(self.playerNumber + 1) + "-" + str(
														 self.direction) + "-" + self.wantTexture,
													 [0.40, 0.625])
				else:
					self.entityRenderer.setImage([0.80, 2],
												 "player-" + str(self.playerNumber + 1) + "-" + str(self.direction) + "-" +  self.wantTexture,
												 [0.40, 0.625])
			self.changeTexture = False

	def display(self):
		self.setCanInteract(False)
		self.wantTexture = ""
		super().display()


	def setLife(self, newLife, death=False):
		super().setLife(newLife, death)

	def applyDamage(self, damage, death=False):
		if self.life == 0:
			if self.em.entities[1 - self.playerNumber].life > 0 :
				if self.takeDamage:
					self.em.entities[1 - self.playerNumber].applyDamage(damage)
					self.takeDamage = False
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
			self.setStun(True)
			self.applyKnockback(ent.knockback, ent.pos)
			self.applyDamage(ent.damage)

		if ent.attributes["interaction"] == 2:
			self.canInteract = True

		super().collision(ent)

	def getItemName(self):
		return self.item.name

	def setCanInteract(self, state):
		self.canInteract = state

	def getCanInteract(self):
		return self.canInteract

	def setItem(self, type):
		if type == "Key":
			from game.game.gameplay import  itemkey
			self.item = itemkey.ItemKey(self)
		elif type == "Weapon":
			from game.game.gameplay import  itemweapon
			self.item = itemweapon.ItemWeapon(self)
		else:
			from game.game.gameplay import item
			self.item = item.Item(self, "Null")

	def setDirection(self, newDirection):
		super().setDirection(newDirection)
		if self.direction != self.oldDirection:
			self.changeTexture = True

	def setWantTexture(self, want):
		self.wantTexture = want
		self.changeTexture = True