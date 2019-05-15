# Object holding by the player to activate padlock

from game.game.gameplay import item
from game.game.entitymodel import triggerbox

class ItemKey(item.Item):
	KEY_USE_TIME = 4  # In frame

	def __init__(self, player):
		super().__init__(player, "Key")

	def useItem(self):
		# Define the pos of the collision box according to the player direction
		if self.player.direction == 0:
			pos = self.player.pos[0] - self.player.halfColSize[0] - 0.15, self.player.pos[1]
		elif self.player.direction == 1:
			pos = [self.player.pos[0], self.player.pos[1]  + self.player.halfColSize[1] + 0.15]
		elif self.player.direction == 2:
			pos = [self.player.pos[0] + self.player.halfColSize[0] + 0.15, self.player.pos[1]]
		else :
			pos = [self.player.pos[0], self.player.pos[1] - self.player.halfColSize[0] - 0.15]

		# Add the temp collision box of key in entityManager

		keyTriggerBox = triggerbox.TriggerBox(self,
											  ["TriggerBox", self.player.em.checkPlace(), pos, ItemKey.KEY_USE_TIME])
		keyTriggerBox.setColBox([0.3, 0.03])
		keyTriggerBox.setCollision(True)
		keyTriggerBox.attributes["key"] = 1
		keyTriggerBox.setEntityMaster(self.player.entityId)
		self.player.em.addWithId(keyTriggerBox)

	def triggerBox(self, ent):
		# Set a null object when the player has used his item
		self.player.setItem("Null")
