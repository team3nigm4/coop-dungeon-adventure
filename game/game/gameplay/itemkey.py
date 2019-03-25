from game.game.gameplay import item
from game.game.entitymodel import triggerbox

class ItemKey(item.Item):

	KEY_USE_TIME = 4

	def __init__(self, player):
		super().__init__(player, "Key")

	def useItem(self):
		if self.player.direction == 0:
			pos = self.player.pos[0] - self.player.halfColSize[0] - 0.15, self.player.pos[1]
			size = [0.3, 0.3]
		elif self.player.direction == 1:
			pos = [self.player.pos[0], self.player.pos[1]  + self.player.halfColSize[1] + 0.15]
			size = [0.3, 0.3]
		elif self.player.direction == 2:
			pos = [self.player.pos[0] + self.player.halfColSize[0] + 0.15, self.player.pos[1]]
			size = [0.3, 0.3]
		else :
			pos = [self.player.pos[0], self.player.pos[1] - self.player.halfColSize[0] - 0.15]
			size = [0.3, 0.03]

		entity = triggerbox.TriggerBox(self, ["TriggerBox", self.player.em.checkPlace(),
												pos, ItemKey.KEY_USE_TIME])

		entity.setColBox(size, True)
		entity.attributes["key"] = 1
		entity.setEntityMaster(self.player.entityId)
		self.player.em.addWithId(entity)

	def triggerBox(self, ent):
		self.player.setItem("Null")
