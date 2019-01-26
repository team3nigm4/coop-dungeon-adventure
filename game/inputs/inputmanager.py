from game.inputs import keyboardmanager as kbm
from game.inputs import mousemanager as mm


class InputManager:
	ESCAPE = 0
	GO_LEFT = 1
	GO_UP = 2
	GO_RIGHT = 3
	GO_DOWN = 4
	INTERACT = 5
	ITEM = 6
	ITEM2 = 7
	RESET = 8

	inputs = None
	type = None
	keyBoardManager = None
	mouseManager = None

	@staticmethod
	def init(input):
		InputManager.inputs = []
		InputManager.type = []
		for i in range(0, len(input)):
			InputManager.inputs.append(input[i][1])
			InputManager.type.append(input[i][0])

		InputManager.keyBoardManager = kbm.KeyBoardManager()
		InputManager.mouseManager = mm.MouseManager()

	@staticmethod
	def input(inpt):
		if InputManager.type[inpt] == 0:
			return kbm.getKey(InputManager.inputs[inpt])
		else:
			return mm.getButton(InputManager.inputs[inpt])

	@staticmethod
	def inputReleased(input):
		if InputManager.type[input] == 0:
			return InputManager.keyBoardManager.keyReleased(InputManager.inputs[input])
		else:
			return InputManager.mouseManager.buttonReleased(InputManager.inputs[input])

	@staticmethod
	def inputPressed(input):
		if InputManager.type[input] == 0:
			return InputManager.keyBoardManager.keyPressed(InputManager.inputs[input])
		else:
			return InputManager.mouseManager.buttonPressed(InputManager.inputs[input])

	@staticmethod
	def dispose():
		for i in range(0, len(InputManager.inputs)):
			if InputManager.type[i] == 0:
				InputManager.keyBoardManager.dispose(InputManager.inputs[i])
			else:
				InputManager.mouseManager.dispose(InputManager.inputs[i])
