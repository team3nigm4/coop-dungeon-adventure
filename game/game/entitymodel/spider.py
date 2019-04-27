# Entity class player, embodies one of the players

from game.game.entityclass import enemy
from game.util import math as mathcda

import random, math


class Spider(enemy.Enemy):
	SPEED_ADD = 0.0027
	SPEED_MAX = 0.07
	SPEED_DECREASE = 0.003

	MOVE_RANGE = 1.5
	MOVE_TIME = 40

	DETECTION_RANGE = 3

	INVINCIBILITY_TIME = 30

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.55, 0.55])
		self.setCollision(True)

		self.attributes["enemyDamage"] = 1
		self.attributes["playerSword"] = 2
		self.attributes["playerBow"] = 2
		self.attributes["collision"] = 1
		self.attributes["heavy"] = 1
		self.attributes["blockDamage"] = 1

		self.direction = 3
		self.damage = 1

		self.initialSpeed = [Spider.SPEED_MAX, Spider.SPEED_MAX]
		self.wantDirection = [0, 0]
		self.maxSpeed = [0, 0]

		self.life = 5
		self.invincibilityTime = Spider.INVINCIBILITY_TIME
		self.knockback = 0.25

		self.target = None
		self.targetCounter = 0
		self.targetDir = [True, True]

		self.entityRenderer.setImage([0.6, 0.6], "spider", [0.3, 0.3])
		self.gapDisplayPos = 0.2

	def update(self):
		super().update()

		if self.target == None:
			if self.targetCounter > Spider.MOVE_TIME:
				self.targetCounter = 0

				# search a target
				track = -1
				di1 = mathcda.distE(self, self.em.entities[self.em.PLAYER_1])
				di2 = mathcda.distE(self, self.em.entities[self.em.PLAYER_2])
				if di1 < di2:
					if  di1 < Spider.DETECTION_RANGE:
						track = self.em.PLAYER_1
				else:
					if  di2 < Spider.DETECTION_RANGE:
						track = self.em.PLAYER_2

				if not track == -1:
					pos = self.em.entities[track].pos
					dist = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
					coef = math.sqrt(dist[0] * dist[0] + dist[1] * dist[1])
					self.target = [self.pos[0] + dist[0] * Spider.MOVE_RANGE / coef, self.pos[1] + dist[1] * Spider.MOVE_RANGE / coef]
					angle = math.acos((self.target[0] - self.pos[0]) / Spider.MOVE_RANGE)

					if self.target[0] > self.pos[0]:
						self.targetDir[0] = True
					else:
						self.targetDir[0] = False

					if self.target[1] > self.pos[1]:
						self.targetDir[1] = True
					else:
						self.targetDir[1] = False

				else:
					angle = random.random() * math.pi * 2
					self.target = [Spider.MOVE_RANGE * math.cos(angle) + self.pos[0], Spider.MOVE_RANGE * math.sin(angle) + self.pos[1]]

					if self.target[0] > self.pos[0]:
						self.targetDir[0] = True
					else:
						self.targetDir[0] = False

					if self.target[1] > self.pos[1]:
						self.targetDir[1] = True
					else:
						self.targetDir[1] = False

				self.maxSpeed = [math.fabs(self.initialSpeed[0] * math.cos(angle)), math.fabs(self.initialSpeed[1] * math.sin(angle))]

			else:
				self.targetCounter +=1
		else:
			if self.targetCounter <= Spider.MOVE_TIME:
				if mathcda.distPx(self.pos[0], self.target[0]) > self.maxSpeed[0]:
					if self.targetDir[0]:
						self.right(2)
					else:
						self.left(2)
				if mathcda.distPy(self.pos[1], self.target[1]) > self.maxSpeed[1]:
					if self.targetDir[1]:
						self.up(2)
					else:
						self.down(2)
				self.targetCounter  +=1
			else:
				self.target = None
				self.targetCounter = 0

		for i in range(2):
			if self.wantDirection[i] == 0:
				if self.speed[i] < 0:
					self.speed[i] += Spider.SPEED_DECREASE
					if self.speed[i] > 0:
						self.speed[i] = 0
						self.inMov[i] = False
				else:
					self.speed[i] -= Spider.SPEED_DECREASE
					if self.speed[i] < 0:
						self.speed[i] = 0
						self.inMov[i] = False
			else:
				self.inMov[i] = True
				self.speed[i] += self.wantDirection[i] * Spider.SPEED_ADD
				if math.fabs(self.speed[i]) > self.maxSpeed[i]:
					self.speed[i] = self.wantDirection[i] * self.maxSpeed[i]

		self.mam.checkCollisionX(self)
		self.mam.checkCollisionY(self)
