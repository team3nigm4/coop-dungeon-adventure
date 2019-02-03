# Class used to change rooms

from game.game.entityclass import entitycollision
from game.game.map import mapmanager


class Door(entitycollision.EntityCollision):

	ARGS_COL_BOX_SIZE = 2
	ARGS_IS_EVENT = 3
	ARGS_EVENT = 4
	ARGS_MAP_ID = 5
	ARGS_MAP_ENTRY_POINT = 6

	def __init__(self, args):
		super().__init__(args)
		self.setColBox(args[Door.ARGS_COL_BOX_SIZE], True)

		if args[Door.ARGS_IS_EVENT]:
			from game.game.map.eventmanager import EventManager
			self.isActive = False
			print(args[Door.ARGS_EVENT])
			EventManager.addActive(args[Door.ARGS_EVENT], self.id)
			mapmanager.MapManager.changeInterMapSize(self.pos, self.halfColSize, 1)

		else:
			self.isActive = True

		self.isTwo = False
		self.attributes["door"] = 2

	def update(self):
		self.isTwo = False

	def collision(self, ent):
		if self.isActive:
			if not self.isTwo:
				self.isTwo = True
				print("collision")
				# Temp system without both players
			else:
				pass
				# Change the map with its id

	def activate(self):
		self.isActive = True
		mapmanager.MapManager.changeInterMapSize(self.pos, self.halfColSize, 0)

	def deactivate(self):
		self.isActive = False
		mapmanager.MapManager.changeInterMapSize(self.pos, self.halfColSize, 1)