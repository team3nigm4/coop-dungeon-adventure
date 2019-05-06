# This class performs the display and the update of the client

from game.inputs.inputmanager import InputManager as im
from game.screen.screens import screen
from game.render.text import text
from game.render.gui import button

from game.render.shape import guirenderer
from game.screen import gamemanager


class CreditsScreen(screen.Screen):

	def __init__(self, info):
		super().__init__()

		self.title = text.Text("pixel1")
		self.title.setSize(1.3)
		self.title.setColor([1,1,1,1])
		self.title.setPosition([9, 10.5])
		self.title.setText("Coop Dungeon Adventure")

		self.copyleft = text.Text("pixel1")
		self.copyleft.setSize(0.4)
		self.copyleft.setColor([1,1,1,1])
		self.copyleft.setCentering("down-left")
		self.copyleft.setText("(C) 2019 Maxence, Alexandre & Baptiste" + " "*29 + "v.0.1")

		self.credits = text.Text("pixel1")
		self.credits.setSize(0.45)
		self.credits.setColor([1,1,1,1])
		self.credits.setPosition([9, 5.3])
		self.credits.setText("Maxence Bazin\nAlexandre Boin\nBaptiste Aleci")

		self.screenTitle = guirenderer.GuiRenderer()
		self.screenTitle.setImage([18, 12], "screentitle")

		def returnMenu():
			from game.screen import gamemanager
			gamemanager.GameManager.setCurrentScreen("menuscreen", [False])
		
		self.returnMenu = button.Button([7.7, 3.9], [2.45, 0.6], "< Retour", returnMenu)


	def init(self):
		pass

	def update(self):
			# Keys test
			if im.inputPressed(im.ESCAPE):
				from game.main.window import Window
				Window.exit()

			self.returnMenu.update()

	def display(self):
		self.screenTitle.display()
		self.title.display()
		self.copyleft.display()
		self.credits.display()
		self.returnMenu.display()

	def unload(self):
		self.screenTitle.unload()
		self.title.unload()
		self.copyleft.unload()
		self.credits.unload()
		self.returnMenu.unload()

