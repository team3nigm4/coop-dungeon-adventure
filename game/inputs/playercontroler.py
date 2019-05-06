
from game.inputs.inputmanager import InputManager as im

class PlayerController:
	VARIABLES = [[1, 1, "reset"],
				 [2, 9, "left"],
				 [3, 10, "up"],
				 [4, 11, "right"],
				 [5, 12, "down"],
				 [6, 13, "interact"],
				 [7, 14, "useItem"],
				 [8, 15, "useItem2"]]

	def __init__(self):
		self.states = [[False, getattr(NameError, "mro")] for i in range(len(PlayerController.VARIABLES))]
		self.player = 0

		self.tempInputState = [0, 0, 0, 0, 0, 0, 0, 0]
		self.inputState = [0, 0, 0, 0, 0, 0, 0, 0]

		self.multi = False
		self.block = False

	def setPlayer(self, num):
		if num == 0:
			self.player = 0
		else:
			self.player = 1

	def update(self):
		for i in range(len(self.inputState)):
			self.tempInputState[i] = self.inputState[i]

		if not self.block:
			if self.multi:
				key = 0
			else:
				key = self.player

			for i in range(0, len(self.states)):
				if im.input(self.VARIABLES[i][key]):
					# No error
					if im.inputPressed(self.VARIABLES[i][key]):
						self.inputState[i] = 2
					else:
						self.inputState[i] = 3
				else:
					if im.inputReleased(self.VARIABLES[i][key]):
						self.inputState[i] = 1
					else:
						self.inputState[i] = 0

		for i in range(0, len(self.states)):
			if self.states[i][0]:
				self.states[i][1](self.inputState[i])

	def setEntity(self, entity):
		self.entity = entity
		for i in range(len(PlayerController.VARIABLES)):
			if hasattr(entity, PlayerController.VARIABLES[i][2]):
				self.states[i][0] = True
				self.states[i][1] = getattr(self.entity, PlayerController.VARIABLES[i][2])
			else:
				self.states[i][0] = False
