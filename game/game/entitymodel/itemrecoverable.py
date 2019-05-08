# Class item recoverable

from game.game.entityclass import entitydrawable


class ItemRecoverable(entitydrawable.EntityDrawable):
	ARGS_ITEM_TYPE = 3

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([1, 1])
		self.setCollision(True)

		self.setType(args[ItemRecoverable.ARGS_ITEM_TYPE])

		self.attributes["interaction"] = 2
		self.press = False

	def collision(self, ent):
		if ent.attributes["interaction"] == 1:
			if ent.type == "Player":
				playItemName = ent.getItemName()
				ent.setItem(self.itemType)

				if not playItemName == "Null":
					self.setType(playItemName)
				else:
					self.removeEm()

	def setType(self, type):
		self.itemType = type
		if self.itemType == "Key":
			key = "item-key"
		else:
			key = "item-weapon"

		self.entityRenderer.setImage([0.8, 0.8], key, [0.4, 0.4])
