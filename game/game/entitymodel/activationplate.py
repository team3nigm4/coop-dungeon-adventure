# Class activation plate, depend on pressure plate, activator entity

from game.game.entitymodel import pressureplate


class ActivationPlate(pressureplate.PressurePlate):
	ARGS_EVENT_ID = 3

	def __init__(self, args):
		super().__init__(args)
		self.images = ["activation-mark-release",
					"activation-mark-press"]

		self.entityRenderer.setImage([1, 1], self.images[0], [0.5, 0.5])

		self.attributes["heavy"] = 0
		self.attributes["energy"] = 2

	def collision(self, ent):
		if ent.attributes["energy"] == 1:
			super().collision(ent)
