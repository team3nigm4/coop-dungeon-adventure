from game.game.entityclass import entity
from game.game.map.maprender import MapRender as mr


class Decor(entity.Entity):
	ARGS_EVENT = 3
	ARGS_DECOR_DEACTIVATE = 4
	ARGS_DECOR_ACTIVATE = 5

	def __init__(self, args):
		super().__init__(args)
		self.pos[0] = int(self.pos[0])
		self.pos[1] = int(self.pos[1])
		self.event = args[Decor.ARGS_EVENT]
		self.ev.addActive(self.event, self.entityId)
		self.decorDeactivate = args[Decor.ARGS_DECOR_DEACTIVATE]
		self.decorActivate = args[Decor.ARGS_DECOR_ACTIVATE]
		self.active = True
		self.testCol = False

	def activate(self):
		if not self.active:
			if self.decorActivate == "delete":
				mr.deleteDecor(self.decorDeactivate, self.pos[0], self.pos[1])
			else:
				mr.deleteDecor(self.decorDeactivate, self.pos[0], self.pos[1])
				mr.addDecor(self.decorActivate, self.pos[0], self.pos[1])
			self.active = True

	def deactivate(self):
		if self.active:
			if self.decorDeactivate == "delete":
				mr.deleteDecor(self.decorActivate, self.pos[0], self.pos[1])
			else:
				mr.deleteDecor(self.decorDeactivate, self.pos[0], self.pos[1])
				mr.addDecor(self.decorDeactivate, self.pos[0], self.pos[1])
			self.active = False
