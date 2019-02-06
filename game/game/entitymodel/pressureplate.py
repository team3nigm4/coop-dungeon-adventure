# Class pressure plate

from game.game.entityclass import entitydrawable
from game.game.map.eventmanager import EventManager

from PIL import Image as img

class PressurePlate(entitydrawable.EntityDrawable):
	ARGS_EVENT_ID = 2

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([1, 1], True)
		self.images = [img.open("game/resources/textures/entities/pressure-plate-released.png"),
					img.open("game/resources/textures/entities/pressure-plate-press.png")]

		self.entityRenderer.setImage([1, 1], self.images[0], [0.5, 0.5])

		self.attributes["heavy"] = 2
		self.press = False
		self.alwaysPressed = False
		self.charge = True

		self.eventId = args[PressurePlate.ARGS_EVENT_ID]
		EventManager.deactivate(self.eventId)

	def update(self):
		if not self.alwaysPressed:
			if not self.charge:
				self.press = False
				self.entityRenderer.setImage([1, 1], self.images[0], [0.5, 0.5])
				self.charge = True
				EventManager.deactivate(self.eventId)
		self.alwaysPressed = False

	def collision(self, ent):
		if not self.press:
			self.entityRenderer.setImage([1, 1], self.images[1], [0.5, 0.5])
			self.charge = False
			self.press = True
			EventManager.activate(self.eventId)

		self.alwaysPressed = True
