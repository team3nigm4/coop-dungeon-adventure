from game.game.entityclass import entity
from game.game.map.eventmanager import EventManager as ev
from game.game.map.eventmanager import EventManager
from game.game.map.eventmanager import EventManager

class Spawn(entity.Entity):
	ARGS_EVENT = 3
	ARGS_ENTITY_INFO = 4

	def __init__(self, args):
		super().__init__(args)

		self.event = args[Spawn.ARGS_EVENT]
		self.entityInfo = args[Spawn.ARGS_ENTITY_INFO]
		self.hasSpawn = False
		self.testCol = False
		self.checkState()

	def activate(self):
		if not self.hasSpawn:
			self.removeEm(False)
			self.em.addA(self.entityInfo)
			ev.remove(self.event, self.entityId)
			self.hasSpawn = True

	def deactivate(self):
		pass

	def checkState(self):
		EventManager.addActive(self.event, self.entityId)
