# Contains managers used in game and update/display the current screen

from game.render.texture.texturemanager import TextureManager
from game.screen import camera
from game.inputs.inputmanager import InputManager
from game.render.shader.shadermanager import ShaderManager
from game.render.text.textmanager import TextManager
from game.util.logger import Logger
from game.main.config import Config


class GameManager:
	# Can be gamescreen, menuscren, messagescreen
	currentScreen = None
	cam = None

	texManager = None
	inputManager = None

	newScreenName = ""
	changeScreenArgs = []
	wantChangeScreen = False

	@staticmethod
	def init():
		Logger.info("GameManager", "Created")
		
		# Init systems
		TextureManager.init()
		TextManager.init()
		InputManager.init(Config.inputs)
		GameManager.cam = camera.Camera(70.0, [0, 0, -8.572])  # FOV 70, Precise position of cam to render 18 * 12 tiles
		ShaderManager.init()

		GameManager.setCurrentScreen("menuscreen", [True])
		GameManager.createCurrentScreen()

	@staticmethod
	def update():
		if GameManager.wantChangeScreen:
			GameManager.createCurrentScreen()

		GameManager.currentScreen.update()
		
		# Dispose managers after updating the game
		InputManager.dispose()
		ShaderManager.dispose()

	@staticmethod
	def display():
		GameManager.currentScreen.display()

	@staticmethod
	def setCurrentScreen(newName, args):
		GameManager.newScreenName = newName
		GameManager.changeScreenArgs = args
		GameManager.wantChangeScreen = True

	@staticmethod
	def createCurrentScreen():
		# Get
		newName = GameManager.newScreenName
		args = GameManager.changeScreenArgs
		
		# Reset variables
		GameManager.wantChangeScreen = False
		GameManager.changeScreenArgs = []
		GameManager.newScreenName = ""

		# Choose the good screen to instance
		if not GameManager.currentScreen == None:
			GameManager.currentScreen.unload()

		if newName == "menuscreen" or newName == "Menuscreen" or newName == "MenuScreen":
			from game.screen.screens import menuscreen
			
			GameManager.currentScreen = menuscreen.MenuScreen(args)
		elif newName == "messagescreen" or newName == "Messagescreen" or newName == "MessageScreen":
			from game.screen.screens import messagescreen
			
			GameManager.currentScreen = messagescreen.MessageScreen(args)
		elif newName == "GameScreen" or newName == "gamescreen" or newName == "Gamescreen":
			from game.screen.screens import gamescreen
			
			# Load the server game (True) or the local Game (False)
			if args[0]:
				Config.loadServer()
				GameManager.currentScreen = gamescreen.GameScreen([True, Config.server["ip"], Config.server["port"]])
			else:
				GameManager.currentScreen = gamescreen.GameScreen([False])

		GameManager.currentScreen.init()

	@staticmethod
	def unload():
		GameManager.currentScreen.unload()
		ShaderManager.unload()
		TextureManager.unload()
