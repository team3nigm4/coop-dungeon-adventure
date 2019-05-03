# Manages key states

from game.main import window
import glfw

class KeyBoardManager:

	state = [False] * 348
	tempState = [False] * 348

	beginKey = 32

	@staticmethod
	def keyPressed(keyId):
		if KeyBoardManager.state[keyId] == True and KeyBoardManager.tempState[keyId] == False:
			return True
		else:
			return False

	@staticmethod
	def keyReleased(keyId):
		if KeyBoardManager.state[keyId] == False and KeyBoardManager.tempState[keyId] == True:
			return True
		else:
			return False

	@staticmethod
	def getKey(key):
		return glfw.get_key(window.Window.window, key) == 1

	@staticmethod
	def dispose():

		for key in range(KeyBoardManager.beginKey, len(KeyBoardManager.state)):
			KeyBoardManager.tempState[key] = KeyBoardManager.state[key]
			KeyBoardManager.state[key] = KeyBoardManager.getKey(key)
