# Class to display a screen with a custom header and message

from game.inputs.inputmanager import InputManager as im
from game.screen.screens import screen
from game.render.text import text
from game.render.gui import button
from game.render.shape import guirenderer
from game.screen import gamemanager

class MessageScreen(screen.Screen):

	# Create all elements that have to be displayed
	def __init__(self, info):
		super().__init__()

		def returnMenu(): # Function called when the return button is clicked
			from game.screen import gamemanager
			gamemanager.GameManager.setCurrentScreen("menuscreen", [True])

		self.copyleft = text.Text("pixel1")
		self.copyleft.setAll("(Copyleft) 2019 Maxence, Alexandre & Baptiste" + " "*25 + "v.0.1", 0.4, [0, 0], [1, 1, 1, 1], "down-left")

		self.title = text.Text("pixel1")
		self.title.setAll(info[0], 1, [9, 5.1], [1, 1, 1, 1], "")

		self.message = text.Text("pixel1")
		self.message.setAll(info[1], 0.8, [9, 3.8], [1, 1, 1, 1], "")

		self.background = guirenderer.GuiRenderer()
		self.background.setImage([18, 12], "background")
		
		self.screenTitle = guirenderer.GuiRenderer()
		self.screenTitle.setImage([18, 12], "screentitle")

		self.returnMenu = button.Button([7.7, 2.8], [2.45, 0.6], "< Retour", returnMenu)
		
	def init(self):
		pass

	def update(self):
			# Keys test
			if im.inputPressed(im.ESCAPE):
				from game.main.window import Window
				Window.exit()

			# Update button texture on hover
			self.returnMenu.update()

	# Display screen elements every loop turn
	def display(self):
		self.background.display()
		self.screenTitle.display()
		self.title.display()
		self.copyleft.display()
		self.message.display()
		self.returnMenu.display()

	# Unload screen element when they aren't necessary anymore
	def unload(self):
		self.background.unload()
		self.screenTitle.unload()
		self.title.unload()
		self.copyleft.unload()
		self.message.unload()
		self.returnMenu.unload()
