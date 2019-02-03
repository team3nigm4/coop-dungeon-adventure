from game.game.entityclass import entitydrawable

from PIL import Image as img

class PressurePlate(entitydrawable.EntityDrawable):
	def __init__(self, args):
		super().__init__(args)
		self.setColBox([1, 1], True)
		self.images = [img.open("game/resources/textures/entities/pressure-plate.png"),
					   img.open("game/resources/textures/entities/pressed-pressure-plate.png")]

		self.entityRenderer.setImage([1, 1], self.images[0], [0.5, 0.5])

		self.attributes["heavy"] = 2
		self.press = False
		self.alwaysPressed = False
		self.charge = True

	def update(self):
		if not self.alwaysPressed:
			if not self.charge:
				self.press = False
				self.entityRenderer.setImage([1, 1], self.images[0], [0.5, 0.5])
				self.charge = True
		self.alwaysPressed = False

	def active(self, press):
		if not self.press:
			self.entityRenderer.setImage([1, 1], self.images[1], [0.5, 0.5])
			self.charge = False
			self.press = True

		self.alwaysPressed = True