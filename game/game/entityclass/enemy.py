# Entity class player, embodies one of the players

from game.game.entityclass import entitycomplex


class Enemy(entitycomplex.EntityComplex):

	ARGS_IS_EVENT = 3
	ARGS_EVENT = 4

	INVINCIBILITY_TIME = 60

	def __init__(self, args):
		super().__init__(args)
		self.isEvent = args[Enemy.ARGS_IS_EVENT]
		if self.isEvent:
			self.eventID = args[Enemy.ARGS_EVENT]
			self.ev.deactivate(self.eventID)

		import random
		self.setDrawCol(True)
		self.colRenderer.setAttributes(self.colSize, [1 - random.random()/3, random.random()/5, random.random()/5, 0.5])
		self.colRenderer.updateModel(self.pos)

		self.setDisplayLayer(self.em.DISPLAY_MIDDLE)

	def setLife(self, newLife, death=True):
		super().setLife(newLife, death)
		if self.isEvent:
			if self.life <= 0:
				self.ev.activate(self.eventID)
