# Entity class player, embodies one of the players

from game.game.entityclass import entitydrawable
from game.game.map.mapmanager import MapManager as mam
from game.inputs.inputmanager import InputManager as im


class Player(entitydrawable.EntityDrawable):
	SPEED = 0.08

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.7, 0.4], True)
		self.entityDisplayer.setImage([0.8, 1.2], "perso.png", [0.4, 0.2])

	def update(self):
		if im.input(im.GO_LEFT):
			self.setPos([mam.checkCollisionX(self.pos, -Player.SPEED, self.colBoxSize), self.pos[1]])
		if im.input(im.GO_UP):
			self.setPos([self.pos[0], mam.checkCollisionY(self.pos, Player.SPEED, self.colBoxSize)])
		if im.input(im.GO_RIGHT):
			self.setPos([mam.checkCollisionX(self.pos, Player.SPEED, self.colBoxSize), self.pos[1]])
		if im.input(im.GO_DOWN):
			self.setPos([self.pos[0], mam.checkCollisionY(self.pos, -Player.SPEED, self.colBoxSize)])
