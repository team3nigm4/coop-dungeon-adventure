from game.game.entityclass import entity


class EntityCollision(entity.Entity):

	def __init__(self, args):
		super().__init__(args)
		self.colBoxSize = [0,0]

	def setColBox(self, size, test):
		self.colBoxSize = size
		from game.game.entityclass.entitymanager import EntityManager as em
		if test:
			em.addToTest(self.id)
		else:
			em.removeToTest(self.id)

