from game.game.entityclass import entity


class Spawn(entity.Entity):
	ARGS_EVENT = 3
	ARGS_ENTITY_INFO = 4

	def __init__(self, args):
		super().__init__(args)

		self.event = args[Spawn.ARGS_EVENT]

		self.entityInfo = args[Spawn.ARGS_ENTITY_INFO]
		self.hasSpawn = False
		self.testCol = False

		from game.game.map.eventmanager import EventManager
		EventManager.addActive(self.event, self.id)

	def activate(self):
		if not self.hasSpawn:
			from game.game.map.eventmanager import EventManager as ev
			self.em.remove(self.id)
			self.em.addA(self.entityInfo)
			ev.remove(self.event, self.id)
			self.hasSpawn = True

	def deactivate(self):
		pass
