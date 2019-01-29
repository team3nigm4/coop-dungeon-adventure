# Manages mouse states

import glfw

from game.main.window import Window


class MouseManager:
	def __init__(self):
		self.state = [False] * 10
		self.tempState = [False] * 10

	def buttonPressed(self, buttonId):
		if self.state[buttonId] == True and self.tempState[buttonId] == False:
			return True
		else:
			return False

	def buttonReleased(self, buttonId):
		if self.state[buttonId] == False and self.tempState[buttonId] == True:
			return True
		else:
			return False

	@staticmethod
	def getButton(button):
		return glfw.get_mouse_button(Window.window, button) == 1

	def dispose(self, buttonId):
		self.tempState[buttonId] = self.state[buttonId]
		self.state[buttonId] = MouseManager.getButton(buttonId)
