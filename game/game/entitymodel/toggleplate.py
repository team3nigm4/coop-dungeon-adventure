# Class pressure plate

from game.game.entityclass import entitydrawable

from PIL import Image as img


class TogglePlate(entitydrawable.EntityDrawable):
	ARGS_EVENT_ID = 3

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([1, 1])
		self.setCollision(True)
		self.images = [img.open("game/resources/textures/entities/toggle-plate-release.png"),
					img.open("game/resources/textures/entities/toggle-plate-press.png")]

		self.entityRenderer.setImage([1, 1], self.images[0], [0.5, 0.5])

		self.attributes["heavy"] = 2
		self.press = False

		self.eventId = args[TogglePlate.ARGS_EVENT_ID]
		self.ev.deactivate(self.eventId)

	def collision(self, ent):
		if ent.attributes["heavy"] == 1:
			if not self.press:
				self.entityRenderer.setImage([1, 1], self.images[1], [0.5, 0.5])
				self.press = True
				self.ev.activate(self.eventId)
