from game.game.gameplay import item
from game.game.entitymodel import triggerbox


class ItemWeapon(item.Item):

	SWORD_ATTACK_TIME = 24
	SWORD_RELOAD_TIME = 48

	LOW_SPEED_COEF = 3

	def __init__(self, player):
		super().__init__(player, "Weapon")
		self.used = False
		self.useCounter = 0

	def useItem(self):
		if not self.used:
			if self.player.direction == 0:
				entity = triggerbox.TriggerBox(self, ["TriggerBox",
													[self.player.pos[0] - self.player.halfColSize[0] - 0.15,self.player.pos[1]], ItemWeapon.SWORD_ATTACK_TIME])

				size = [0.3, 0.5]
			elif self.player.direction == 1:
				entity = triggerbox.TriggerBox(self, ["TriggerBox",
													[self.player.pos[0], self.player.pos[1] + self.player.halfColSize[1] + 0.15], ItemWeapon.SWORD_ATTACK_TIME])

				size = [0.5, 0.3]
			elif self.player.direction == 2:
				entity = triggerbox.TriggerBox(self, ["TriggerBox",
													[self.player.pos[0] + self.player.halfColSize[0] + 0.15, self.player.pos[1]], ItemWeapon.SWORD_ATTACK_TIME])
				size = [0.3, 0.5]
			else:
				entity = triggerbox.TriggerBox(self, ["TriggerBox",
													[self.player.pos[0], self.player.pos[1] - self.player.halfColSize[0] - 0.15], ItemWeapon.SWORD_ATTACK_TIME])
				size = [0.5, 0.03]

			entity.setColBox(size, True)
			entity.updateColRenderer()
			entity.attributes["playerSword"] = 1
			self.player.em.add(entity)
			self.player.maxSpeed /= ItemWeapon.LOW_SPEED_COEF

			self.used = True

	def update(self):
		if self.used:
			if self.useCounter == ItemWeapon.SWORD_ATTACK_TIME:
				self.player.maxSpeed *= ItemWeapon.LOW_SPEED_COEF
			if self.useCounter == ItemWeapon.SWORD_RELOAD_TIME:
				self.useCounter = 0
				self.used = False
			else :
				self.useCounter +=1


	def triggerBox(self, ent):
		ent.setLife(ent.life - self.player.damage)
