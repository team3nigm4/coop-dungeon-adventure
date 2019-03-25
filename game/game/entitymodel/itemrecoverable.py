# Class item recoverable

from game.game.entityclass import entitydrawable


class ItemRecoverable(entitydrawable.EntityDrawable):
	ARGS_ITEM_TYPE = 3

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([1, 1], True)

		self.setType(args[ItemRecoverable.ARGS_ITEM_TYPE])

		self.attributes["heavy"] = 2
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
			path = "/entities/item-key.png"
		else:
			path = "/entities/item-weapon.png"

		self.entityRenderer.setImagePath([0.8, 0.8], path, [0.4, 0.4])
