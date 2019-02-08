# Class used to change rooms

from game.game.entityclass import entitycollision
from game.game.map.mapmanager import MapManager as mam


class Door(entitycollision.EntityCollision):

	ARGS_COL_BOX_SIZE = 2
	ARGS_ZONE_NAME = 3
	ARGS_MAP_ID = 4
	ARGS_MAP_ENTRY_POINT = 5
	ARGS_IS_EVENT = 6
	ARGS_EVENT = 7

	def __init__(self, args):
		super().__init__(args)
		self.setColBox(args[Door.ARGS_COL_BOX_SIZE], False)

		self.zone = args[Door.ARGS_ZONE_NAME]
		self.map = args[Door.ARGS_MAP_ID]
		self.entry = args[Door.ARGS_MAP_ENTRY_POINT]

		self.isEvent = args[Door.ARGS_IS_EVENT]
		if self.isEvent:
			self.isActive = False
			self.event = args[Door.ARGS_EVENT]
		else:
			self.isActive = True
			self.setColBox(self.colSize, True)

		self.isTwo = False
		self.attributes["door"] = 2

	def update(self):
		self.isTwo = False

	def collision(self, ent):
		if self.isActive:
			if not self.isTwo:
				self.isTwo = True
				# Temp system without both players
				mam.unloadImages()
				mam.reserveChange([self.zone, self.map, self.entry])
			else:
				pass
				# Change the map with its id

	def activate(self):
		self.isActive = True
		self.setColBox(self.colSize, True)
		mam.changeInterMapSize(self.pos, self.halfColSize, 0)

	def deactivate(self):
		self.isActive = False
		self.setColBox(self.colSize, False)
		mam.changeInterMapSize(self.pos, self.halfColSize, 1)

	def setId(self, id):
		super().setId(id)
		if self.isEvent:
			from game.game.map.eventmanager import EventManager
			self.isActive = False
			EventManager.addActive(self.event, self.id)
			mam.changeInterMapSize(self.pos, self.halfColSize, 1)

		else:
			self.isActive = True
