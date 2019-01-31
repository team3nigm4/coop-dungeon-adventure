# Entity class to display something

from game.game.entityclass import entitycollision
from game.game import entityrenderer as ed


class EntityDrawable(entitycollision.EntityCollision):

	def __init__(self, args):
		super().__init__(args)
		self.entityDisplayer = ed.EntityRenderer()

	def display(self):
		self.entityDisplayer.display()

	def setPos(self, position):
		super().setPos(position)
		self.entityDisplayer.updateModel(self.pos)

	def unload(self):
		self.entityDisplayer.unload()
