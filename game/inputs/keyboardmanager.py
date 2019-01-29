# Manages key states


from game.main.window import Window
import glfw


class KeyBoardManager:
	def __init__(self):
		self.state = [False] * 350
		self.tempState = [False] * 350

	def keyPressed(self, keyId):
		if self.state[keyId] == True and self.tempState[keyId] == False:
			return True
		else:
			return False

	def keyReleased(self, keyId):
		if self.state[keyId] == False and self.tempState[keyId] == True:
			return True
		else:
			return False

	@staticmethod
	def getKey(key):
		return glfw.get_key(Window.window, key) == 1

	def dispose(self, keyId):
		self.tempState[keyId] = self.state[keyId]
		self.state[keyId] = KeyBoardManager.getKey(keyId)
