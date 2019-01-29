# Entity class to display something

from game.game import entity
from game.game import entityrenderer as ed


class EntityDrawable(entity.Entity):

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
