# Class pressure plate

from game.game.entitymodel import pressureplate
from game.game.map.eventmanager import EventManager

from PIL import Image as img

class ActivationPlate(pressureplate.PressurePlate):
	ARGS_EVENT_ID = 2

	def __init__(self, args):
		super().__init__(args)
		self.images = [img.open("game/resources/textures/entities/activation-plate-release.png"),
					img.open("game/resources/textures/entities/activation-plate-press.png")]

		self.entityRenderer.setImage([1, 1], self.images[0], [0.5, 0.5])

		self.attributes["heavy"] = 0
		self.attributes["energy"] = 2

	def collision(self, ent):
		if ent.attributes["energy"] == 1:
			if not self.press:

				# em.remove(ent.id)

				self.entityRenderer.setImage([1, 1], self.images[1], [0.5, 0.5])
				self.charge = False
				self.press = True
				EventManager.activate(self.eventId)

			self.alwaysPressed = True
