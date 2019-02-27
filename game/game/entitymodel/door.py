# Class used to change rooms

from game.game.entityclass import entitycollision


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
			self.setDrawCol(True)

		self.isTwo = False
		self.attributes["door"] = 2

		self.colRenderer.setAttributes(self.colSize, [0.7725, 0.956, 0.258, 0.5])


	def update(self):
		self.isTwo = False

	def collision(self, ent):
		if self.isActive:
			if ent.attributes["door"] == 1:
				if not self.isTwo:
					self.isTwo = True
					# Temp system without both players
				else:
					self.mam.unloadImages()
					self.mam.reserveChange([self.zone, self.map, self.entry])
					# Change the map with its id

	def activate(self):
		self.isActive = True
		self.setColBox(self.colSize, True)
		self.mam.setTileSize(self.pos, self.halfColSize, 0)
		self.setDrawCol(True)

	def deactivate(self):
		self.isActive = False
		self.setColBox(self.colSize, False)
		self.mam.setTileSize(self.pos, self.halfColSize, 1)
		self.setDrawCol(False)

	def setId(self, id):
		super().setId(id)
		if self.isEvent:
			self.isActive = False
			self.ev.addActive(self.event, self.id)
			self.mam.setTileSize(self.pos, self.halfColSize, 1)

		else:
			self.isActive = True
