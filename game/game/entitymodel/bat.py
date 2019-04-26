# Entity class player, embodies one of the players

from game.game.entityclass import enemy
from game.util import math as mathcda

import math


class Bat(enemy.Enemy):
	SPEED_ADD = 0.003
	SPEED_MAX = 0.035
	SPEED_DECREASE = 0.003

	DETECTION_RANGE = 4

	INVINCIBILITY_TIME = 60

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.9, 0.9])
		self.setCollision(True)

		self.attributes["enemyDamage"] = 1
		self.attributes["playerSword"] = 2
		self.attributes["playerBow"] = 2

		self.direction = 3
		self.maxSpeed = [Bat.SPEED_MAX, Bat.SPEED_MAX]
		self.targetId = self.entityId
		self.speedCounter = 0

		self.life = 7
		self.damage = 1
		self.invincibilityTime = Bat.INVINCIBILITY_TIME
		self.knockback = 0.35
		self.height = 0.8

		self.entityRenderer.setImage([1, 1], "bat", [0.5, 0.5])
		self.gapDisplayPos = -1

	def update(self):
		super().update()
		# Target detection
		if self.targetId.getId() == self.entityId.getId():
			if mathcda.distE(self, self.em.entities[self.em.PLAYER_1]) < Bat.DETECTION_RANGE:
				self.targetId = self.em.entities[self.em.PLAYER_1].entityId
			elif mathcda.distE(self, self.em.entities[self.em.PLAYER_2]) < Bat.DETECTION_RANGE:
				self.targetId = self.em.entities[self.em.PLAYER_2].entityId
		else:
			target = self.em.entities[self.targetId.getId()]
			if target.getId() == -1:
				self.targetId = self.entityId
			else:
				# Apply the effect of a bat flying
				self.maxSpeed = [Bat.SPEED_MAX - Bat.SPEED_MAX * math.cos(self.speedCounter) * 0.30,
								 Bat.SPEED_MAX - Bat.SPEED_MAX * math.cos(self.speedCounter) * 0.30]
				self.speedCounter += 0.13
				if self.speedCounter >= 2 * math.pi:
					self.speedCounter = 0

				# Bat want to move if too far of the player
				if mathcda.distEx(self, target) > self.maxSpeed[0]:
					if self.pos[0] > target.pos[0]:
						self.left(2)
					else:
						self.right(2)

				if mathcda.distEy(self, target) > self.maxSpeed[1]:
					if self.pos[1] > target.pos[1]:
						self.down(2)
					else:
						self.up(2)

		# Update position
		for i in range(2):
			if self.wantDirection[i] == 0:
				if self.speed[i] < 0:
					self.speed[i] += Bat.SPEED_DECREASE
					if self.speed[i] > 0:
						self.speed[i] = 0
						self.inMov[i] = False
				else:
					self.speed[i] -= Bat.SPEED_DECREASE
					if self.speed[i] < 0:
						self.speed[i] = 0
						self.inMov[i] = False
			else:
				self.inMov[i] = True
				self.speed[i] += self.wantDirection[i] * Bat.SPEED_ADD
				if math.fabs(self.speed[i]) > self.maxSpeed[i]:
					self.speed[i] = self.wantDirection[i] * self.maxSpeed[i]

		self.setPos([self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]])

	def collision(self, ent):
		if (ent.attributes["playerSword"] == 1 and self.attributes["playerSword"] == 2) or \
				(ent.attributes["playerBow"] == 1 and self.attributes["playerBow"] == 2):
			# If it is another player giving the damage
			if not ent.entityId == self.targetId and ent.giveDamage:
				# This player is the new target
				self.targetId = ent.getMaster()
			ent.triggerBox(self)
