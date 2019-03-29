# Entity class player, embodies one of the players

from game.game.entityclass import enemy

class Mannequin(enemy.Enemy):
	ARGS_LIFE = 5

	INVINCIBILITY_TIME = 60

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.6, 0.4])
		self.setCollision(True)

		self.entityRenderer.setImagePath([1, 1.5], "entities/mannequin.png", [0.45, 0.2])

		self.attributes["playerSword"] = 2
		self.attributes["playerBow"] = 2
		self.attributes["blockDamage"] = 1

		self.life = args[Mannequin.ARGS_LIFE]

		self.invincibilityTime = Mannequin.INVINCIBILITY_TIME

	def applyKnockback(self, knockback, pos):
		pass
