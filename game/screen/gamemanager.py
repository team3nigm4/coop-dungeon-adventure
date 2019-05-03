# Contains game's managers (and camera), asks functions update (server/client) and display(client)

from game.render.texture.texturemanager import TextureManager as tm
from game.screen import camera
from game.inputs.inputmanager import InputManager as im
from game.render.shader.shadermanager import ShaderManager as sm
from game.render.text.textmanager import TextManager as txm
from game.util.logger import Logger


class GameManager:
	currentScreen = None
	cam = None

	texManager = None
	inputManager = None

	@staticmethod
	def init():
		# Init systems
		Logger.info("GAME MANAGER", "Created")

		tm.init()
		txm.init()

		from game.main.config import Config
		im.init(Config.inputs)

		GameManager.cam = camera.Camera(70.0, [0, 0, -8.572])  # Precise position of cam to render 18 * 12 tiles
		sm.init()

		GameManager.setCurrentScreen("menuscreen", [True])

	@staticmethod
	def update():
		GameManager.currentScreen.update()
		im.dispose()
		sm.dispose()

	@staticmethod
	def display():
		GameManager.currentScreen.display()

	@staticmethod
	def setCurrentScreen(value, arg):
		if not GameManager.currentScreen == None:
			GameManager.currentScreen.unload()

		if value == "menuscreen" or value == "Menuscreen" or value == "MenuScreen":
			from game.screen.screens import menuscreen as me
			GameManager.currentScreen = me.MenuScreen([])
		elif value == "GameScreen" or value == "gamescreen" or value == "Gamescreen":
			from game.screen.screens import gamescreen as ga
			if arg[0] == True:
				import json
				info = json.load(open("data/server/server.json"))
				GameManager.currentScreen = ga.GameScreen([True, info["ip"], info["port"]])
			else:
				GameManager.currentScreen = ga.GameScreen([False])
			# cdi-p08.cda-game.ga 34141
			# play.cda-game.ga 34141
			# alex.cda-game.ga
			# localhost 34141

		GameManager.currentScreen.init()

	@staticmethod
	def unload():
		GameManager.currentScreen.unload()
		sm.unload()
		tm.unload()
		tm.endState()
