from game.game.gameplay import item
from game.game.entitymodel import triggerbox
from game.game.entitymodel import arrow


class ItemWeapon(item.Item):
	SWORD_ATTACK_TIME = 24
	SWORD_RELOAD_TIME = 48

	BOW_RELOAD_TIME = 48

	LOW_SPEED_COEF = 3

	def __init__(self, player):
		super().__init__(player, "Weapon")
		self.used = False
		self.useCounter = 0
		self.trigBox = triggerbox.TriggerBox(self, ["TriggerBox",[0,0], 0])
		# True sword, False bow

		self.arm = True
		if self.player.em.len > 0:
			if self.player.em.entities[1 - self.player.playerNumber].item.name == "Weapon":
				if self.player.em.entities[1 - self.player.playerNumber].item.arm:
					self.arm = False
				else:
					self.arm = True


	def useItem(self):
		if not self.used:
			if self.arm:
				if self.player.direction == 0:
					size = [0.5, 0.5]
				elif self.player.direction == 1:
					size = [0.5, 0.6]
				elif self.player.direction == 2:
					size = [0.5, 0.5]
				else:
					size = [0.5, 0.6]

				entity = triggerbox.TriggerBox(self, ["TriggerBox", self.triggerPos(), ItemWeapon.SWORD_ATTACK_TIME])

				entity.setColBox(size, True)
				#entity.updateColRenderer()

				entity.attributes["playerSword"] = 1
				self.trigBox = entity

				self.player.em.add(entity)
				self.player.maxSpeed /= ItemWeapon.LOW_SPEED_COEF

			else:
				entity = arrow.Arrow(["Arrow", [self.player.pos[0], self.player.pos[1] + 0.5], self.player.direction])
				self.player.em.add(entity)

			self.used = True

	def useItem2(self):
		if not self.used:
			if not self.player.em.entities[1-self.player.playerNumber].item.name == "Weapon":
				if self.arm:
					self.arm = False
					print("Player", str(self.player.playerNumber), "switch arm to bow")
				else:
					self.arm = True
					print("Player", str(self.player.playerNumber), "Switch arm to sword")

	def update(self):
		if self.used:
			if self.arm:
				if self.useCounter <= ItemWeapon.SWORD_ATTACK_TIME:
					self.trigBox.setPos(self.triggerPos())
					if self.useCounter == ItemWeapon.SWORD_ATTACK_TIME:
						self.player.maxSpeed *= ItemWeapon.LOW_SPEED_COEF

				if self.useCounter == ItemWeapon.SWORD_RELOAD_TIME:
					self.useCounter = 0
					self.used = False
				else:
					self.useCounter += 1
			else:
				if self.useCounter < ItemWeapon.BOW_RELOAD_TIME:
					self.useCounter += 1
				else:
					self.used = False
					self.useCounter = 0


	def triggerPos(self):
		if self.player.direction == 0:
			return [self.player.pos[0] - self.player.halfColSize[0] - 0.26, self.player.pos[1]]

		elif self.player.direction == 1:
			return [self.player.pos[0],  self.player.pos[1] + self.player.halfColSize[1] + 0.3]

		elif self.player.direction == 2:
			return [self.player.pos[0] + self.player.halfColSize[0] + 0.26, self.player.pos[1]]
		else:
			return [self.player.pos[0], self.player.pos[1] - self.player.halfColSize[0] - 0.31]

	def triggerBox(self, ent):
		ent.applyDamage(self.player.damage)
