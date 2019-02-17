from game.game.entityclass import entitycollision


class TriggerBox(entitycollision.EntityCollision):

	ARGS_COUNTER = 2

	def __init__(self, entity, args):
		super().__init__(args)
		self.maxCount = args[TriggerBox.ARGS_COUNTER]
		self.count = 0
		self.entity = entity

		self.setDrawCol(True)
		self.colRenderer.setAttributes(self.colSize, [0, 0, 1, 1])

	def update(self):
		super().update()
		if self.count >= self.maxCount:
			self.em.remove(self.id, False)

		self.count +=1

	def triggerBox(self, ent):
		self.entity.triggerBox(ent)
