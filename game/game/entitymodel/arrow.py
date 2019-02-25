# Entity class player, embodies one of the players

import math

from game.game.entityclass import entitycomplex

class Arrow(entitycomplex.EntityComplex):
	SPEED = 0.2
	DAMAGE = 1

	ARGS_DIRECTION = 2

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.2, 0.4], True)

		self.attributes["playerBow"] = 1
		self.direction = args[Arrow.ARGS_DIRECTION]
		if self.direction == 0:
			self.speed[0] = -Arrow.SPEED
		elif self.direction == 1:
			self.speed[1] = Arrow.SPEED
		elif self.direction == 2:
			self.speed[0] = Arrow.SPEED
		else:
			self.speed[1] = -Arrow.SPEED

		self.entityRenderer.setImagePath([1, 1], "entities/arrow.png", [0.5, 0.5])

	def update(self):
		super().update()

		if not self.speed[0] == 0:
			self.mam.checkCollisionX(self)
		if not self.speed[1] == 0:
			self.mam.checkCollisionY(self)

		if self.oldPos == self.pos:
			self.em.remove(self.id)
		self.wantDirection = [0, 0]


	def triggerBox(self, ent):
		ent.applyDamage(self.DAMAGE)
		self.setLife(0)