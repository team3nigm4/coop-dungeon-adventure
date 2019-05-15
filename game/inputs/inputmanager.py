# Static class to manage every input from key and mouse

from game.inputs.keyboardmanager import KeyBoardManager as kbm
from game.inputs.mousemanager import MouseManager as mm


class InputManager:
	ESCAPE = 0
	RESET = 1
	GO_LEFT_0 = 2
	GO_UP_0 = 3
	GO_RIGHT_0 = 4
	GO_DOWN_0 = 5
	INTERACT_0 = 6
	ITEM_0 = 7
	ITEM2_0 = 8
	GO_LEFT_1 = 9
	GO_UP_1 = 10
	GO_RIGHT_1 = 11
	GO_DOWN_1 = 12
	INTERACT_1 = 13
	ITEM_1 = 14
	ITEM2_1 = 15
	
	inputs = None
	type = None

	@staticmethod
	def init(inpt):
		# Reservs some inputs for player inputs
		actions = ["ECHAP", "RESET", "GO_LEFT_0", "GO_UP_0", "GO_RIGHT_0", "GO_DOWN_0", "INTERACT_0", "ITEM_0", "ITEM2_0",
		 "GO_LEFT_1", "GO_UP_1", "GO_RIGHT_1", "GO_DOWN_1", "INTERACT_1", "ITEM_1", "ITEM2_1"]

		InputManager.inputs = []
		InputManager.type = []
		for i in range(0, len(actions)):
			InputManager.inputs.append(inpt[actions[i]][0][1])
			InputManager.type.append(inpt[actions[i]][0][0])

	@staticmethod
	def input(inpt):
		if InputManager.type[inpt] == 0:
			return kbm.getKey(InputManager.inputs[inpt])
		else:
			return mm.getButton(InputManager.inputs[inpt])

	@staticmethod
	def inputReleased(inpt):
		if InputManager.type[inpt] == 0:
			return kbm.keyReleased(InputManager.inputs[inpt])
		else:
			return mm.buttonReleased(InputManager.inputs[inpt])

	@staticmethod
	def inputPressed(inpt):
		if InputManager.type[inpt] == 0:
			return kbm.keyPressed(InputManager.inputs[inpt])
		else:
			return mm.buttonPressed(InputManager.inputs[inpt])

	# Get state of each inputs iin a table
	@staticmethod
	def getState():
		import math
		values = []
		for i in range(1, len(InputManager.inputs)):
			key = 0
			if InputManager.type[i] == 0:
				if kbm.state[InputManager.inputs[i]]:
					key += 3
				if kbm.tempState[InputManager.inputs[i]]:
					key -= 1
					key = math.fabs(key)
			else:
				if mm.state[InputManager.inputs[i]]:
					key += 3
				if mm.tempState[InputManager.inputs[i]]:
					key -= 1
					key = math.fabs(key)

			values.append(key)
		return values

	@staticmethod
	def dispose():
		kbm.dispose()
		mm.dispose()
