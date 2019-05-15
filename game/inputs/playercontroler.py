# Class to interact between the player(and its inputs) and an entity

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
		# Use this
		self.block = False

	# In multi, define the player controlled by this controller
	# The player number "choose" the inputs of the controller(see VARIABLES)
	def setPlayer(self, num):
		if num == 0:
			self.player = 0
		elif num == 1:
			self.player = 1

	def update(self):
		for i in range(len(self.inputState)):
			self.tempInputState[i] = self.inputState[i]

		if not self.block:
			# In multi, the test keys will be those of player 1
			# regardless of the real number of player controller
			if self.multi:
				key = 0
			else:
				key = self.player

			# Different num for each state of key
			# 0 is key releasing
			# 1 is key pressed (1 frame)
			# 2 is key pressing (1 frame after)
			# 3 is key release (1 frame)
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

		# Call the function with the state of the key
		for i in range(0, len(self.states)):
			if self.states[i][0]:
				self.states[i][1](self.inputState[i])

	# Set an entity controlled by this class
	def setEntity(self, entity):
		self.entity = entity

		# During this loop see if the entity contains functions with name like in VARIABLES (ex : right() )
		# to call it when the key associated is press
		for i in range(len(PlayerController.VARIABLES)):
			if hasattr(entity, PlayerController.VARIABLES[i][2]):
				self.states[i][0] = True
				self.states[i][1] = getattr(self.entity, PlayerController.VARIABLES[i][2])
			else:
				self.states[i][0] = False
