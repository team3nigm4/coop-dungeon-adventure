# Class to manage key states

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

	# Get the state of a key
	@staticmethod
	def getKey(key):
		if KeyBoardManager.beginKey <= key <= 348:
			return KeyBoardManager.state[key]
		else:
			return False

	# Test the state of a key in the legit range
	@staticmethod
	def testState(key):
		if KeyBoardManager.beginKey <= key <= 348:
			return glfw.get_key(window.Window.window, key) == 1
		else:
			return False

	# Reload the state of each key possible
	@staticmethod
	def dispose():
		for key in range(KeyBoardManager.beginKey, len(KeyBoardManager.state)):
			KeyBoardManager.tempState[key] = KeyBoardManager.state[key]
			KeyBoardManager.state[key] = KeyBoardManager.testState(key)
