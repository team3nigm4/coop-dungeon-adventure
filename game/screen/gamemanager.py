# Contains game's managers (and camera), asks functions update (server/client) and display(client)

from game.render.texture import texturemanager as textureManager
from game.screen import camera
from game.inputs.inputmanager import InputManager as im
from game.render.shader.shadermanager import ShaderManager as sm


class GameManager:
	MENUSCREEN = 0
	GAMESCREEN = 1

	# server = True

	currentScreen = None
	cam = None

	texManager = None
	inputManager = None

	# Data for games
	serverData = [0]
	clientData = [0]

	def __init__(self):

		# Init systems
		GameManager.texManager = textureManager.TextureManager()
		GameManager.texManager.init()

		from game.main.config import Config

		im.init(Config.inputs)

		GameManager.cam = camera.Camera(70.0, [0, 0, -8.572])  # Precise position of cam to render 18 * 12 tiles

		sm.init()

	def begin(self):
		self.setCurrentScreen(GameManager.GAMESCREEN)

	# if GameManager.server:
	# 	Server.init()

	def update(self):
		# if GameManager.server:
		# 	Server.update()
		self.currentScreen.update()
		im.dispose()

		sm.updateLink(sm.TEXTURE, "view", GameManager.cam.getView())

	def display(self):
		GameManager.currentScreen.display()

	def setCurrentScreen(self, value):
		if value == GameManager.MENUSCREEN:
			from game.screen.screens import menuScreen as me
			GameManager.currentScreen = me.MenuScreen()
		if value == GameManager.GAMESCREEN:
			from game.screen.screens import gamescreen as ga
			GameManager.currentScreen = ga.GameScreen()
		# if GameManager.server:
		# 	Server.init()

	def unload(self):
		GameManager.currentScreen.unload()
		GameManager.texManager.error.unload()
		GameManager.texManager.endState()
		sm.unload()
