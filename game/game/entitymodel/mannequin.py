# Entity class player, embodies one of the players

from game.game.entityclass import entitycomplex
from game.game.map.mapmanager import MapManager as mam


class Mannequin(entitycomplex.EntityComplex):
	ARGS_LIFE = 2
	INVINCIBILITY_TIME = 60

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.6, 0.4], True)

		self.entityRenderer.setImagePath([1, 1.5], "entities/mannequin.png", [0.45, 0.2])

		self.attributes["collision"] = 0
		self.attributes["player1Damage"] = 2
		self.attributes["player2Damage"] = 2

		self.setDrawCol(True)
		self.colRenderer.setAttributes(self.colSize, [0, 1, 0, 1])

		self.invincibilityTime = Mannequin.INVINCIBILITY_TIME


	def collision(self, ent):
		if ent.attributes["playerSword"] == 1 or ent.attributes["playerBow"] == 1:
			ent.triggerBox(self)

		super().collision(ent)
