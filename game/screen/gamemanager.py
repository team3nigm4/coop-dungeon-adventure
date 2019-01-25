# Contains game's managers (and camera), asks functions update (server/client) and display(client)

from game.render.texture import texturemanager as textureManager
from game.screen import camera

class GameManager:
	currentScreen = "null"

	MENUSCREEN = 0
	GAMESCREEN = 1
	texManager = "null"
	cam = "null"

	def __init__(self):

		#Init systems
		GameManager.texManager = textureManager.TextureManager()
		GameManager.texManager.init()
		GameManager.cam = camera.Camera(70.0, [0, 0, -8.572]) # Precise position of cam to render 18 * 12 tiles

		self.setCurrentScreen(GameManager.GAMESCREEN)
		
	def update(self):
		GameManager.currentScreen.update()

	def display(self):
		GameManager.currentScreen.display()

	def setCurrentScreen(self, value):
		if value == GameManager.MENUSCREEN:
			from game.screen.screens import menuScreen as me
			GameManager.currentScreen = me.MenuScreen()
		if value == GameManager.GAMESCREEN:
			from game.screen.screens import gamescreen as ga
			GameManager.currentScreen = ga.GameScreen()

	def unload(self):
		GameManager.currentScreen.unload()
		GameManager.texManager.error.unload()
		GameManager.texManager.endState()
