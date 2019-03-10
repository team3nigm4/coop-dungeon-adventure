# Class sliding block

from game.game.entityclass import entitydrawable


class SlidingBlock(entitydrawable.EntityDrawable):
	SPEED = 0.20

	DAMAGE = 2

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.998, 0.998], True)
		self.entityRenderer.setImagePath([1, 1], "entities/sliding-block.png", [0.5, 0.5])

		self.attributes["collision"] = 2
		self.attributes["heavy"] = 1
		self.attributes["interaction"] = 2

		self.setDisplayLayer(self.em.DISPLAY_DOWN2)

	def update(self):
		super().update()
		if self.inMov[0]:
			self.mam.checkCollisionX(self)

			if self.oldPos == self.pos:
				self.inMov[0] = False
				self.speed[0] = 0

		elif self.inMov[1]:
			self.mam.checkCollisionY(self)

			if self.oldPos == self.pos:
				self.inMov[1] = False
				self.speed[1] = 0

		self.mam.checkEmpty(self)

	def collision(self, ent):
		# If we apply the collision
		if ent.attributes["collision"] > 0 and (ent.attributes["collision"] != 2 or ent.inMov[0] or ent.inMov[1]):
			# Just move in x
			if ent.inMov[0] and not ent.inMov[1]:
				tempDir = 0
				if ent.speed[0] > 0:
					ent.setPos([self.pos[0] - self.halfColSize[0] - ent.halfColSize[0] - 0.002, ent.pos[1]])
					tempDir = 1
				elif ent.speed[0] < 0:
					ent.setPos([self.pos[0] + self.halfColSize[0] + ent.halfColSize[0] + 0.002, ent.pos[1]])
					tempDir = -1

				if ent.attributes["collision"] == 2:
					ent.inMov[0] = 0

				# interaction attribute
				if ent.attributes["interaction"] == 1:
					self.inMov[0] = True
					self.speed[0] = SlidingBlock.SPEED * tempDir

			# Just move in y
			elif ent.inMov[1] and not ent.inMov[0]:
				tempDir = 0
				if ent.speed[1] < 0:
					ent.setPos([ent.pos[0], self.pos[1] + self.halfColSize[1] + ent.halfColSize[1] + 0.002])
					tempDir = -1
				elif ent.speed[1] > 0:
					ent.setPos([ent.pos[0], self.pos[1] - self.halfColSize[1] - ent.halfColSize[1] - 0.002])
					tempDir = 1

				if ent.attributes["collision"] == 2:
					ent.inMov[1] = 0

				# interaction attribute
				if ent.attributes["interaction"] == 1:
					self.inMov[1] = True
					self.speed[1] = SlidingBlock.SPEED * tempDir

			# Move in both coordinates
			elif ent.inMov[0] and ent.inMov[1]:
				oldPos = [ent.pos[0] - ent.speed[0], ent.pos[1] - ent.speed[1]]

				# what ent's position to replace
				if ent.inMov[0]:
					# left
					if oldPos[0] + ent.halfColSize[0] < self.pos[0] - self.halfColSize[0]:
						ent.setPos([self.pos[0] - self.halfColSize[0] - ent.halfColSize[0] - 0.002, ent.pos[1]])
					# right
					elif oldPos[0] - ent.halfColSize[0] > self.pos[0] + self.halfColSize[0]:
						ent.setPos([self.pos[0] + self.halfColSize[0] + ent.halfColSize[0] + 0.002, ent.pos[1]])

				if ent.inMov[1]:
					# up
					if oldPos[1] - ent.halfColSize[1] > self.pos[1] + self.halfColSize[1]:
						ent.setPos([ent.pos[0], self.pos[1] + self.halfColSize[1] + ent.halfColSize[1] + 0.002])
					# down
					elif oldPos[1] + ent.halfColSize[1] < self.pos[1] - self.halfColSize[1]:
						ent.setPos([ent.pos[0], self.pos[1] - self.halfColSize[1] - ent.halfColSize[1] - 0.002])

		if self.inMov[0] or self.inMov[1]:
			if ent.attributes["blockDamage"] == 1:
				if self.inMov[0]:
					if self.speed[0] > 0:
						if ent.pos[0] > self.pos[0]:
							ent.applyDamage(SlidingBlock.DAMAGE)
					else:
						if ent.pos[0] < self.pos[0]:
							ent.applyDamage(SlidingBlock.DAMAGE)
				else:
					if self.speed[1] > 0:
						if ent.pos[1] > self.pos[1]:
							ent.applyDamage(SlidingBlock.DAMAGE)
					else:
						if ent.pos[1] < self.pos[1]:
							ent.applyDamage(SlidingBlock.DAMAGE)
