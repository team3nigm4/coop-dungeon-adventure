# Class pressure plate

from game.game.entitymodel import toggleplate
from game.game.map.eventmanager import EventManager

from PIL import Image as img


class PressurePlate(toggleplate.TogglePlate):

	def __init__(self, args):
		super().__init__(args)
		self.images = [img.open("game/resources/textures/entities/pressure-plate-released.png"),
					img.open("game/resources/textures/entities/pressure-plate-press.png")]

		self.entityRenderer.setImage([1, 1], self.images[0], [0.5, 0.5])
		self.alwaysPressed = False
		self.charge = True

	def update(self):
		if not self.alwaysPressed:
			if not self.charge:
				self.press = False
				self.entityRenderer.setImage([1, 1], self.images[0], [0.5, 0.5])
				self.charge = True
				EventManager.deactivate(self.eventId)
		self.alwaysPressed = False

	def collision(self, ent):
		super().collision(ent)
		self.alwaysPressed = True
		self.charge = False
