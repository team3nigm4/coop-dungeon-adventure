
from game.inputs.inputmanager import InputManager as im

class PlayerController:
	VARIABLES = [[2, 9, "left"],
				 [3, 10, "up"],
				 [4, 11, "right"],
				 [5, 12, "down"],
				 [6, 13, "interact"],
				 [7, 14, "item"],
				 [8, 15, "item2"]]

	def __init__(self):
		self.states =  [[False, getattr(NameError, "mro")] for i in range(len(PlayerController.VARIABLES))]
		self.player = 0

	def setPlayer(self, num):
		if num == 0:
			self.player = 0
		else:
			self.player = 1

	def update(self):
		for i in range(0, len(self.states)):
			if self.states[i][0]:
				if im.input(self.VARIABLES[i][self.player]):
					# No error
					if im.inputPressed(self.VARIABLES[i][self.player]):
						self.states[i][1](2)
					else:
						self.states[i][1](3)
				else:
					if im.inputReleased(self.VARIABLES[i][self.player]):
						self.states[i][1](1)
					else:
						self.states[i][1](0)


	def setEntity(self, entity):
		self.entity = entity
		for i in range(len(PlayerController.VARIABLES)):
			if hasattr(entity, PlayerController.VARIABLES[i][2]):
				self.states[i][0] = True
				self.states[i][1] = getattr(self.entity, PlayerController.VARIABLES[i][2])
			else:
				self.states[i][0] = False
