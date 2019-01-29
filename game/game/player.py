# Entity class player, embodies one of the players

from game.game import entitydrawable
from game.game.mapmanager import MapManager as mam
from game.inputs.inputmanager import InputManager as im


class Player(entitydrawable.EntityDrawable):
	SPEED = 0.08

	def __init__(self, args):
		self.colBoxSize = [0.7, 0.4]
		args.append([self.colBoxSize[0] / 2, self.colBoxSize[1] / 2])
		super().__init__(args)

	def update(self):
		if im.input(im.GO_LEFT):
			self.setPos([mam.checkCollisionX(self.pos, -Player.SPEED, self.colBoxSize), self.pos[1]])
		if im.input(im.GO_UP):
			self.setPos([self.pos[0], mam.checkCollisionY(self.pos, Player.SPEED, self.colBoxSize)])
		if im.input(im.GO_RIGHT):
			self.setPos([mam.checkCollisionX(self.pos, Player.SPEED, self.colBoxSize), self.pos[1]])
		if im.input(im.GO_DOWN):
			self.setPos([self.pos[0], mam.checkCollisionY(self.pos, -Player.SPEED, self.colBoxSize)])

	def addPos(self, addPos):
		self.pos[0] += addPos[0]
		self.pos[1] += addPos[1]
		self.updateModel()
