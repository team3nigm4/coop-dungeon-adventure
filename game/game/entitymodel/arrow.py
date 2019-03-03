# Entity class player, embodies one of the players

import math

from game.game.entityclass import entitycomplex

class Arrow(entitycomplex.EntityComplex):
	SPEED = 0.2
	DAMAGE = 1

	ARGS_DIRECTION = 3

	def __init__(self, args):
		super().__init__(args)

		self.attributes["playerBow"] = 1
		self.direction = args[Arrow.ARGS_DIRECTION]
		if self.direction == 0:
			self.setColBox([0.4, 0.2], True)
			self.speed[0] = -Arrow.SPEED
		elif self.direction == 1:
			self.setColBox([0.2, 0.4], True)
			self.speed[1] = Arrow.SPEED
		elif self.direction == 2:
			self.setColBox([0.4, 0.2], True)
			self.speed[0] = Arrow.SPEED
		else:
			self.setColBox([0.2, 0.4], True)
			self.speed[1] = -Arrow.SPEED

		self.entityRenderer.setImagePath([1, 1], "entities/arrow.png", [0.5, 0.5])
		self.setDisplayLayer(self.em.DISPLAY_MIDDLE)

		self.setDrawCol(True)
		self.colRenderer.setAttributes(self.colSize, [0, 0, 1, 0.5])
		self.colRenderer.updateModel(self.pos)

	def update(self):
		super().update()

		if not self.speed[0] == 0:
			self.mam.checkCollisionX(self)
		if not self.speed[1] == 0:
			self.mam.checkCollisionY(self)

		if self.oldPos == self.pos:
			self.em.remove(self.id)
		self.wantDirection = [0, 0]

	def collision(self, ent):
		if ent.attributes["collision"] == 2:
			self.setLife(0)

	def triggerBox(self, ent):
		ent.applyDamage(self.DAMAGE)
		self.setLife(0)
