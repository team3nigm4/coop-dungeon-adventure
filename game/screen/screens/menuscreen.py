# This class performs the display and the update of the client

from game.inputs.inputmanager import InputManager as im
from game.screen.screens import screen
from game.render.text import text
from game.render.gui import button


class MenuScreen(screen.Screen):

	def __init__(self, info):
		super().__init__()

		self.text = text.Text("pixel1")
		self.text.setSize(1.3)
		self.text.setColor([1,1,1,1])
		self.text.setPosition([9, 10.5])
		self.text.setText("Coop Dungeon Adventure")

		def gameLocal():
			from game.screen import gamemanager
			gamemanager.GameManager.setCurrentScreen("gamescreen", [False])

		def gameMulti():
			from game.screen import gamemanager
			gamemanager.GameManager.setCurrentScreen("gamescreen", [True])

		self.playLocal = button.Button([9, 6], [5, 1], "Local", gameLocal)

		self.playMulti = button.Button([9, 4], [5, 1], "Mutltijoueur", gameMulti)

	def init(self):
		pass

	def update(self):
			# Keys test
			if im.inputPressed(im.ESCAPE):
				from game.main.window import Window
				Window.exit()

			self.playLocal.update()
			self.playMulti.update()

	def display(self):
		self.text.display()
		self.playLocal.display()
		self.playMulti.display()

	def unload(self):
		self.text.unload()
		self.playLocal.unload()
		self.playMulti.unload()

