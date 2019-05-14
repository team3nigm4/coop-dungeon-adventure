# Class for a bit more complex entity, parent class for every entity with interactions

from game.game.entityclass import entity


class EntityCollision(entity.Entity):

	def __init__(self, args):
		super().__init__(args)
		self.colSize = [1, 1]
		self.halfColSize = [0.5, 0.5]
		self.inMov = [False, False]
		self.speed = [0, 0]
		self.oldPos = self.pos
		self.testCol = False

		# NO_STATE = 0
		# GIVE_STATE = 1
		# ex : player has interaction to 1
		# TAKE_STATE = 2
		# ex: sliding block has interaction to 2
		self.attributes = {
			"collision": 0,
			"door": 0,
			"enemyDamage": 0,
			"energy": 0,
			"heavy": 0,
			"interaction": 0,
			"key": 0,
			"playerSword": 0,
			"playerBow": 0,
			"blockDamage": 0,
		}

		# Create a box renderer for every entity collision
		from game.render.shape import boxrenderer
		self.drawCol = False
		color = [0.1, 0.1, 0.1, 0.4]
		self.colRenderer = boxrenderer.BoxRenderer(self.colSize, color)
		self.colRenderer.updateModel([round(self.pos[0] * 32) / 32, round(self.pos[1] * 32) / 32])

	def setDrawCol(self, state):
		self.drawCol = state
		if self.drawCol:
			self.colRenderer.setAttributes(self.colSize, self.colRenderer.color)
			self.colRenderer.updateModel([round(self.pos[0] * 32) / 32, round(self.pos[1] * 32) / 32])

	def dispose(self):
		self.oldPos = self.pos

	def displayBox(self):
		if self.drawCol:
			self.colRenderer.display()

	def setColBox(self, size):
		self.colSize = size
		self.halfColSize[0] = self.colSize[0] / 2
		self.halfColSize[1] = self.colSize[1] / 2

		if self.drawCol:
			self.colRenderer.setAttributes(self.colSize, self.colRenderer.color)
			self.colRenderer.updateModel([round(self.pos[0] * 32) / 32, round(self.pos[1] * 32) / 32])

	def setCollision(self, state):
		old = self.testCol
		self.testCol = state
		if not self.entityId.id == -1:
			if self.testCol and not old:
				self.em.addToTest(self.entityId)
			elif not self.testCol and old:
				self.em.removeToTest(self.entityId)

	def colReduc(self):
		self.setColBox([self.colSize[0] - 0.002, self.colSize[1] - 0.002])

	def setPos(self, position):
		super().setPos(position)
		# Also set the position of the renderer
		self.colRenderer.updateModel([round(self.pos[0] * 32) / 32, round(self.pos[1] * 32) / 32])

	def setSpeed(self, speed):
		self.speed = speed

	def collision(self, ent):
		pass

	def unload(self):
		self.em.removeToTest(self.entityId)
