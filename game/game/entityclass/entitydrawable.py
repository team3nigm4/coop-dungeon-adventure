# Entity class to display something

from game.game.entityclass import entitycollision
from game.game import entityrenderer as ed


class EntityDrawable(entitycollision.EntityCollision):

	def __init__(self, args):
		super().__init__(args)
		self.entityRenderer = ed.EntityRenderer()
		self.setPos(self.pos)

	def display(self):
		self.entityRenderer.display()

	def setPos(self, position):
		super().setPos(position)
		self.entityRenderer.updateModel(self.pos)

	def unload(self):
		self.entityRenderer.unload()
