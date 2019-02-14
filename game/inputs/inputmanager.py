# Manage every input from the player

from game.inputs import keyboardmanager as kbm
from game.inputs import mousemanager as mm


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
	keyBoardManager = None
	mouseManager = None

	@staticmethod
	def init(inpt):
		actions = ["ECHAP", "RESET", "GO_LEFT_0", "GO_UP_0", "GO_RIGHT_0", "GO_DOWN_0", "INTERACT_0", "ITEM_0", "ITEM2_0",
		 "GO_LEFT_1", "GO_UP_1", "GO_RIGHT_1", "GO_DOWN_1", "INTERACT_1", "ITEM_1", "ITEM2_1"]

		InputManager.inputs = []
		InputManager.type = []
		for i in range(0, len(actions)):
			InputManager.inputs.append(inpt[actions[i]][0][1])
			InputManager.type.append(inpt[actions[i]][0][0])

		InputManager.keyBoardManager = kbm.KeyBoardManager()
		InputManager.mouseManager = mm.MouseManager()

	@staticmethod
	def input(inpt):
		if InputManager.type[inpt] == 0:
			return kbm.KeyBoardManager.getKey(InputManager.inputs[inpt])
		else:
			return mm.MouseManager.getButton(InputManager.inputs[inpt])

	@staticmethod
	def inputReleased(inpt):
		if InputManager.type[inpt] == 0:
			return InputManager.keyBoardManager.keyReleased(InputManager.inputs[inpt])
		else:
			return InputManager.mouseManager.buttonReleased(InputManager.inputs[inpt])

	@staticmethod
	def inputPressed(inpt):
		if InputManager.type[inpt] == 0:
			return InputManager.keyBoardManager.keyPressed(InputManager.inputs[inpt])
		else:
			return InputManager.mouseManager.buttonPressed(InputManager.inputs[inpt])

	@staticmethod
	def getState():
		import math
		values = []
		for i in range(1, len(InputManager.inputs)):
			key = 0
			if InputManager.type[i] == 0:
				if InputManager.keyBoardManager.state[InputManager.inputs[i]]:
					key += 3
				if InputManager.keyBoardManager.tempState[InputManager.inputs[i]]:
					key -= 1
					key = math.fabs(key)
			else:
				if InputManager.mouseManager.state[InputManager.inputs[i]]:
					key += 3
				if InputManager.mouseManager.tempState[InputManager.inputs[i]]:
					key -= 1
					key = math.fabs(key)

			values.append(key)
		return values

	@staticmethod
	def dispose():
		for i in range(0, len(InputManager.inputs)):
			if InputManager.type[i] == 0:
				InputManager.keyBoardManager.dispose(InputManager.inputs[i])
			else:
				InputManager.mouseManager.dispose(InputManager.inputs[i])
