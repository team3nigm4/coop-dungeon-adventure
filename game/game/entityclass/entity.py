from game.game.entityclass import entitymanager
from game.game.map import eventmanager
from game.game.map import mapmanager


class Entity:
	ARGS_TYPE = 0
	ARGS_ID = 1
	ARGS_POSITION = 2

	def __init__(self, args):
		self.type = args[Entity.ARGS_TYPE]
		self.id = args[Entity.ARGS_ID]
		self.pos = args[Entity.ARGS_POSITION]

		self.em = entitymanager.EntityManager
		self.ev = eventmanager.EventManager
		self.mam = mapmanager.MapManager

	def setPos(self, position):
		self.pos = position

	def update(self):
		pass

	def display(self):
		pass

	def displayBox(self):
		pass

	def setId(self, id):
		self.id = id

	def unload(self):
		pass
