# Class used to change rooms

from game.game.entityclass import entitycollision
from game.game.map.maprender import MapRender as mr


class Tp(entitycollision.EntityCollision):

	ARGS_COL_BOX_SIZE = 3
	ARGS_ZONE_NAME = 4
	ARGS_MAP_ID = 5
	ARGS_MAP_ENTRY_POINT = 6
	ARGS_IS_EVENT = 7
	ARGS_EVENT = 8

	def __init__(self, args):
		super().__init__(args)
		self.setColBox(args[Tp.ARGS_COL_BOX_SIZE])
		self.zone = args[Tp.ARGS_ZONE_NAME]
		self.map = args[Tp.ARGS_MAP_ID]
		self.entry = args[Tp.ARGS_MAP_ENTRY_POINT]

		self.isEvent = args[Tp.ARGS_IS_EVENT]

		if self.isEvent:
			self.event = args[Tp.ARGS_EVENT]
			self.ev.addActive(self.event, self.entityId)
			self.setCollision(True)
		else:
			self.setDrawCol(True)
			self.setCollision(True)

		self.isTwo = False
		self.attributes["door"] = 2

		self.colRenderer.setAttributes(self.colSize, [0.7725, 0.956, 0.258, 0.5])

		if self.colSize[0] > self.colSize[1]:
			if self.pos[1] > len(mr.tilesPosition[0]) / 2:
				self.exitPos = 1
			else:
				self.exitPos = 3
		else:
			if self.pos[0] > len(mr.tilesPosition[0][0]) / 2:
				self.exitPos = 2
			else:
				self.exitPos = 0

	def update(self):
		self.isTwo = False

	def collision(self, ent):
		if ent.attributes["door"] == 1:
			if not self.isTwo:
				self.isTwo = True
			else:
				# Change the map with its values
				self.mam.reserveChange(self.zone, self.map, self.entry, self.exitPos)

	def activate(self):
		if not self.testCol:
			self.setCollision(True)
			self.setDrawCol(True)

	def deactivate(self):
		if self.testCol:
			self.setCollision(False)
			self.setDrawCol(False)
