from game.game.entityclass import entity


class EntityCollision(entity.Entity):

	# NO_STATE = 0
	# GIVE_STATE = 1
	# TAKE_STATE = 2

	def __init__(self, args):
		super().__init__(args)
		self.colSize = [1, 1]
		self.halfColSize = [0.5, 0.5]
		self.inMov = [False, False]
		self.speed = [0, 0]
		self.oldPos = self.pos
		self.testCol = False

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

		from game.render.shape import boxrenderer
		self.drawCol = False
		color = [0.1, 0.1, 0.1,  0.4]
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

	def setColBox(self, size, test, remove=True):
		self.colSize = size
		self.halfColSize[0] = self.colSize[0] / 2
		self.halfColSize[1] = self.colSize[1] / 2

		self.testCol = test
		if not self.id == -1:
			if self.testCol:
				self.em.addToTest(self.id)
			else:
				if remove:
					self.em.removeToTest(self.id)

		if self.drawCol:
			self.colRenderer.setAttributes(self.colSize, self.colRenderer.color)
			self.colRenderer.updateModel([round(self.pos[0] * 32) / 32, round(self.pos[1] * 32) / 32])

	def setPos(self, position):
		super().setPos(position)
		self.colRenderer.updateModel([round(self.pos[0] * 32) / 32, round(self.pos[1] * 32) / 32])

	def setSpeed(self, speed):
		self.speed = speed

	def collision(self, ent):
		pass
