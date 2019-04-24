from game.game.entityclass import entitycollision


class TriggerBox(entitycollision.EntityCollision):

	ARGS_COUNTER = 3

	def __init__(self, entity, args):
		super().__init__(args)
		self.maxCount = args[TriggerBox.ARGS_COUNTER]
		self.count = 0
		self.entity = entity
		self.entityMaster = -1

		self.setDrawCol(True)
		self.colRenderer.setAttributes(self.colSize, [0, 0, 1, 0.5])

		self.giveDamage = True

	def update(self):
		super().update()
		if self.count >= self.maxCount:
			self.removeEm(False)

		self.count +=1

	def setEntityMaster(self, entityMaster):
		self.entityMaster = entityMaster

	def getMaster(self):
		return self.entityMaster

	def triggerBox(self, ent):
		self.entity.triggerBox(ent)
