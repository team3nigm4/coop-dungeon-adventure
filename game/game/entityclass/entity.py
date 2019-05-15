# Parent class of every entity if the game

from game.game.entityclass import entitymanager
from game.game.map import eventmanager
from game.game.map import mapmanager
from game.game.entityclass import entityid
from game.util import logger


class Entity:
	ARGS_TYPE = 0
	ARGS_ID = 1
	ARGS_POSITION = 2

	def __init__(self, args):
		# Set base variables
		self.type = args[Entity.ARGS_TYPE]
		self.entityId = entityid.EntityId()
		self.entityId.setId(args[Entity.ARGS_ID])
		self.pos = args[Entity.ARGS_POSITION]

		# Set base short name
		self.em = entitymanager.EntityManager
		self.ev = eventmanager.EventManager
		self.mam = mapmanager.MapManager
		self.log = logger.Logger

	def setPos(self, position):
		self.pos = position

	def setId(self, id):
		self.entityId.setId(id)

	def getId(self):
		return self.entityId.getId()

	# Remove easily from entity Manager
	def removeEm(self, printRemove=True):
		self.em.remove(self.entityId, printRemove)

	# Unused methods but use by every entity and called by many managers
	# Must be here

	def update(self):
		pass

	def display(self):
		pass

	def dispose(self):
		pass

	def displayBox(self):
		pass

	def unload(self):
		pass
