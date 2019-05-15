# Object holding by the player to attack with the sword or the bow enemies

from game.game.gameplay import item
from game.game.entitymodel import triggerbox
from game.game.entitymodel import arrow


class ItemWeapon(item.Item):
	# In frame
	SWORD_ATTACK_TIME = 24
	SWORD_RELOAD_TIME = 48
	BOW_RELOAD_TIME = 72

	# In tile
	SWORD_KNOCKBACK = 0.10


	SWORD_ATTACK_DAMAGE = 2

	# For sword
	LOW_SPEED_COEF = 3

	def __init__(self, player):
		super().__init__(player, "Weapon")
		self.used = False
		self.useCounter = 0
		# Init an useless triggerBox to prevent bugs
		self.swordTriggerBox = triggerbox.TriggerBox(self, ["TriggerBox", -1, [0, 0], 0])

		# True sword, False bow
		self.arm = True

		# Is the other player is here
		if self.player.em.len >= 1:
			# If the other player hold a weapon item
			if self.player.em.entities[1 - self.player.playerNumber].item.getName() == "Weapon":
				# Set the opposite of his arm
				self.arm ^= self.player.em.entities[1 - self.player.playerNumber].item.arm

	def useItem(self):
		if not self.used:
			# Sword
			if self.arm:
				self.swordTriggerBox = triggerbox.TriggerBox(self, ["TriggerBox", self.player.em.checkPlace(),
																	self.defSwordTiggerBoxPos(),
																	ItemWeapon.SWORD_ATTACK_TIME])
				self.swordTriggerBox.setColBox([1, 1])
				self.swordTriggerBox.setCollision(True)
				self.swordTriggerBox.attributes["playerSword"] = 1
				self.swordTriggerBox.setEntityMaster(self.player.entityId)

				self.player.em.addWithId(self.swordTriggerBox)
				# When the player use his item, he must walk slower
				self.player.maxSpeed /= ItemWeapon.LOW_SPEED_COEF
				# And the player must display his texture with a sword
				self.player.setWantTexture("sword")
			# Bow
			else:
				# When the player use his item, spawn an arrow
				ar = arrow.Arrow(["Arrow", self.player.em.checkPlace(), [self.player.pos[0], self.player.pos[1] + 0.5], self.player.direction])
				ar.setEntityMaster(self.player.entityId)
				self.player.em.addWithId(ar)
				# And the player must display his texture with a bow
				self.player.setWantTexture("bow")

			self.used = True

	# Switch item between the sword and the bow, if the other hasn't a weapon
	def useItem2(self):
		if not self.used:
			if not self.player.em.entities[1 - self.player.playerNumber].item.getName() == "Weapon":
				# Sword
				if self.arm:
					self.arm = False
					print("Player", str(self.player.playerNumber), "Switch weapon to the bow")
				# Bow
				else:
					self.arm = True
					print("Player", str(self.player.playerNumber), "Switch weapon to the sword")

	def update(self):
		if self.used:
			# Sword
			if self.arm:
				# The player must display his texture with a sword
				self.player.setWantTexture("sword")
				# Sword use counter
				if self.useCounter <= ItemWeapon.SWORD_ATTACK_TIME:
					# Reset the pos of the sword trigger box according to the current player position, and direction
					self.swordTriggerBox.setPos(self.defSwordTiggerBoxPos())
					if self.useCounter == ItemWeapon.SWORD_ATTACK_TIME:
						self.player.maxSpeed *= ItemWeapon.LOW_SPEED_COEF

				if self.useCounter == ItemWeapon.SWORD_RELOAD_TIME:
					self.useCounter = 0
					self.used = False
					self.player.setWantTexture("")
				else:
					self.useCounter += 1
			# Bow
			else:
				# The player must display his texture with a bow
				self.player.setWantTexture("bow")
				if self.useCounter < ItemWeapon.BOW_RELOAD_TIME:
					self.useCounter += 1
				else:
					self.used = False
					self.useCounter = 0
					self.player.setWantTexture("")

	# Define the sword trigger box position according to the player position and direction
	def defSwordTiggerBoxPos(self):
		if self.player.direction == 0:
			return [self.player.pos[0] - self.player.halfColSize[0] - self.swordTriggerBox.halfColSize[0],
					self.player.pos[1] + 0.3]

		elif self.player.direction == 1:
			return [self.player.pos[0],  self.player.pos[1] + self.player.halfColSize[1] + 0.4]

		elif self.player.direction == 2:
			return [self.player.pos[0] + self.player.halfColSize[0] + self.swordTriggerBox.halfColSize[0],
					self.player.pos[1] + 0.3]
		else:
			return [self.player.pos[0], self.player.pos[1] - self.player.halfColSize[0] - 0.31]

	# When the sword touch an enemy
	def triggerBox(self, ent):
		ent.setStun(True)

		if self.player.direction == 0:
			ent.applyKnockback(ItemWeapon.SWORD_KNOCKBACK, [ent.pos[0] + 1, ent.pos[1]])
		elif self.player.direction == 1:
			ent.applyKnockback(ItemWeapon.SWORD_KNOCKBACK, [ent.pos[0], ent.pos[1] - 1])
		elif self.player.direction == 2:
			ent.applyKnockback(ItemWeapon.SWORD_KNOCKBACK, [ent.pos[0] - 1, ent.pos[1]])
		elif self.player.direction == 3:
			ent.applyKnockback(ItemWeapon.SWORD_KNOCKBACK, [ent.pos[0], ent.pos[1] + 1])

		ent.applyDamage(ItemWeapon.SWORD_ATTACK_DAMAGE)
