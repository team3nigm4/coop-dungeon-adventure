# Manages mouse states

import glfw

from game.main import window
from game.main.config import Config


class MouseManager:
	state = [False] * 7
	tempState = [False] * 7

	oldMousePos = [0, 0]
	mousePos = [0, 0]

	oldMousePosRelative = [0, 0]
	mousePosRelative = [0, 0]

	@staticmethod
	def buttonPressed(buttonId):
		if MouseManager.state[buttonId] == True and MouseManager.tempState[buttonId] == False:
			return True
		else:
			return False

	@staticmethod
	def buttonReleased(buttonId):
		if MouseManager.state[buttonId] == False and MouseManager.tempState[buttonId] == True:
			return True
		else:
			return False

	@staticmethod
	def getButton(button):
		return glfw.get_mouse_button(window.Window.window, button) == 1

	@staticmethod
	def dispose():
		MouseManager.oldMousePos = MouseManager.mousePos
		MouseManager.mousePos = list(glfw.get_cursor_pos(window.Window.window))
		MouseManager.mousePos[1] = Config.values["window"]["height"] - MouseManager.mousePos[1]

		MouseManager.oldMousePosRelative = MouseManager.mousePosRelative
		MouseManager.mousePosRelative = [MouseManager.mousePos[0] / Config.values["window"]["width"] * 18
			, MouseManager.mousePos[1] / Config.values["window"]["height"] * 12]

		for key in range(len(MouseManager.state)):
			MouseManager.tempState[key] = MouseManager.state[key]
			MouseManager.state[key] = MouseManager.getButton(key)

	@staticmethod
	def getMousePosRelative():
		return MouseManager.mousePosRelative
