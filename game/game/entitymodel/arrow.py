# Entity class player, embodies one of the players

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
			self.setColBox([0.4, 0.2])
			self.speed[0] = -Arrow.SPEED
		elif self.direction == 1:
			self.setColBox([0.2, 0.4])
			self.speed[1] = Arrow.SPEED
		elif self.direction == 2:
			self.setColBox([0.4, 0.2])
			self.speed[0] = Arrow.SPEED
		else:
			self.setColBox([0.2, 0.4])
			self.speed[1] = -Arrow.SPEED

		self.setCollision(True)

		self.entityRenderer.setImage([1, 1], "arrow-" + str(self.direction), [0.5, 0.5])
		self.setDisplayLayer(self.em.DISPLAY_MIDDLE)

		self.setDrawCol(True)
		self.colRenderer.setAttributes(self.colSize, [0, 0, 1, 0.5])
		self.colRenderer.updateModel(self.pos)
		self.gapDisplayPos = -1
		self.entityMaster = -1
		self.giveDamage = True

		self.knockback = 0.25

	def update(self):
		super().update()

		if not self.speed[0] == 0:
			self.mam.checkCollisionX(self)
		if not self.speed[1] == 0:
			self.mam.checkCollisionY(self)

		if self.oldPos == self.pos:
			self.removeEm(False)
		self.wantDirection = [0, 0]

	def collision(self, ent):
		if ent.attributes["collision"] == 2:
			self.setLife(0)

	def setEntityMaster(self, entityMaster):
		self.entityMaster = entityMaster

	def getMaster(self):
		return self.entityMaster

	def triggerBox(self, ent):
		if self.giveDamage:
			ent.setStun(True)
			if self.direction == 0:
				ent.applyKnockback(self.knockback, [ent.pos[0] + 1, ent.pos[1]])
			elif self.direction == 1:
				ent.applyKnockback(self.knockback, [ent.pos[0], ent.pos[1] - 1])
			elif self.direction == 2:
				ent.applyKnockback(self.knockback, [ent.pos[0] - 1, ent.pos[1]])
			elif self.direction == 3:
				ent.applyKnockback(self.knockback, [ent.pos[0], ent.pos[1] + 1])

			self.giveDamage = False
			ent.applyDamage(self.DAMAGE)
			self.setLife(0)
