# Parent class for entity which can display with a renderer

from game.game.entityclass import entitycollision
from game.render.shape import entityrenderer as ed
from game.util.logger import Logger


class EntityDrawable(entitycollision.EntityCollision):
	def __init__(self, args):
		super().__init__(args)
		# Init attributes
		self.displayLayer = -1
		self.setDisplayLayer(self.em.DISPLAY_DOWN)
		self.entityRenderer = ed.EntityRenderer()
		self.setPos(self.pos)
		self.direction = 0
		self.oldDirection = 0
		# Variable use in the depth calculation with other entities to define who is under who
		self.gapDisplayPos = 0

	def display(self):
		self.entityRenderer.display()

	def setDirection(self, newDirection):
		self.oldDirection = self.direction
		self.direction = newDirection

	def setPos(self, position):
		super().setPos(position)
		# Also set the position of the renderer
		self.entityRenderer.updateModel([round(self.pos[0] * 32) / 32, round(self.pos[1] * 32) / 32])

		# If display layer is middle, check the position of the entity
		if self.displayLayer == self.em.DISPLAY_MIDDLE:
			self.em.displayMiddleEntity(self.entityId)

	# Define to which layer will be displayed the entity
	def setDisplayLayer(self, layer):
		if self.displayLayer != layer:
			# Delete the old id registered if the class was registered
			if not self.displayLayer == -1:
				self.em.removeToDipslay(self.displayLayer, self.entityId)

			# Security
			if layer >= 0 and layer <= 2:
				self.displayLayer = layer
				self.em.addToDisplay(self.displayLayer, self.entityId)
			else:
				Logger.error("EnDrawable",
							 "Invalid layer (" + str(layer) + ") for " + str(self.type) + " with id " + str(id))
		
	def unload(self):
		super().unload()
		self.entityRenderer.unload()
		if 0 <= self.displayLayer <= 2:
			self.em.removeToDipslay(self.displayLayer, self.entityId)
