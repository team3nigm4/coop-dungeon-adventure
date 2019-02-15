from game.game.entityclass import entitycollision


class TriggerBox(entitycollision.EntityCollision):

	ARGS_COUNTER = 2

	def __init__(self, entity, args):
		super().__init__(args)
		self.maxCount = args[TriggerBox.ARGS_COUNTER] * 60
		self.count = 0
		self.entity = entity

	def update(self):
		super().update()
		if self.count >= self.maxCount :
			print(self.id)
			self.em.remove(self.id)

		self.count +=1

	def triggerBox(self):
		self.entity.triggerBox()