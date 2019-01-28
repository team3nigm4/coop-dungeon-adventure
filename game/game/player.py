from game.game import entitydrawable
from game.inputs.inputmanager import InputManager as im

class Player(entitydrawable.EntityDrawable):

	SPEED = 0.08

	def __init__(self, args):
		super().__init__(args)

	def update(self):
		if im.input(im.GO_LEFT):
			self.addPos([-Player.SPEED, 0])
		if im.input(im.GO_UP):
			self.addPos([0, Player.SPEED])
		if im.input(im.GO_RIGHT):
			self.addPos([Player.SPEED, 0])
		if im.input(im.GO_DOWN):
			self.addPos([0, -Player.SPEED])


	def addPos(self, addPos):
		self.pos[0] += addPos[0]
		self.pos[1] += addPos[1]
		self.updateModel()