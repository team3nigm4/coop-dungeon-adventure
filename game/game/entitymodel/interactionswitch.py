from game.game.entityclass import entity

class InteractionSwitch(entity.Entity):
	ARGS_SIZE = 3
	ARGS_EVENT = 4
	ARGS_INTERACTION_ID_DEACTIVATE = 5
	ARGS_INTERACTION_ID_ACTIVATE = 6

	def __init__(self, args):
		super().__init__(args)
		self.size = args[InteractionSwitch.ARGS_SIZE]
		self.halfSize = [self.size[0] / 2 - 0.001, self.size[1] / 2 - 0.01]
		self.event = args[InteractionSwitch.ARGS_EVENT]
		self.ev.addActive(self.event, self.entityId)
		self.idActivate = args[InteractionSwitch.ARGS_INTERACTION_ID_ACTIVATE]
		self.idDeactivate = args[InteractionSwitch.ARGS_INTERACTION_ID_DEACTIVATE]
		self.active = True
		self.testCol = False

	def activate(self):
		if not self.active:
			if not self.idActivate == -1:
				self.mam.setTileSize(self.pos, self.halfSize, self.idActivate)
				self.active = True

	def deactivate(self):
		if self.active:
			if not self.idDeactivate == -1:
				self.mam.setTileSize(self.pos, self.halfSize, self.idDeactivate)
				self.active = False
