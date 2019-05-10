# This class performs the display and the update of the client

from game.inputs.inputmanager import InputManager as im
from game.screen.screens import screen
from game.render.text import text
from game.render.gui import button

from game.render.shape import guirenderer
from game.screen import gamemanager


class MessageScreen(screen.Screen):

	def __init__(self, info):
		super().__init__()

		self.copyleft = text.Text("pixel1")
		self.copyleft.setSize(0.4)
		self.copyleft.setColor([1,1,1,1])
		self.copyleft.setCentering("down-left")
		self.copyleft.setText("(C) 2019 Maxence, Alexandre & Baptiste" + " "*29 + "v.0.1")

		self.title = text.Text("pixel1")
		self.title.setSize(1)
		self.title.setColor([1,1,1,1])
		self.title.setPosition([9, 5.1])
		self.title.setText(info[0])

		self.message = text.Text("pixel1")
		self.message.setSize(0.8)
		self.message.setColor([1,1,1,1])
		self.message.setPosition([9, 3.8])
		self.message.setText(info[1])

		self.background = guirenderer.GuiRenderer()
		self.background.setImage([18, 12], "background")
		
		self.screenTitle = guirenderer.GuiRenderer()
		self.screenTitle.setImage([18, 12], "screentitle")

		def returnMenu():
			from game.screen import gamemanager
			gamemanager.GameManager.setCurrentScreen("menuscreen", [True])
		
		self.returnMenu = button.Button([7.7, 2.8], [2.45, 0.6], "< Retour", returnMenu)

	def init(self):
		pass

	def update(self):
			# Keys test
			if im.inputPressed(im.ESCAPE):
				from game.main.window import Window
				Window.exit()

			self.returnMenu.update()

	def display(self):
		self.background.display()
		self.screenTitle.display()
		self.title.display()
		self.copyleft.display()
		self.title.display()
		self.message.display()
		self.returnMenu.display()

	def unload(self):
		self.background.unload()
		self.screenTitle.unload()
		self.title.unload()
		self.copyleft.unload()
		self.title.unload()
		self.message.unload()
		self.returnMenu.unload()

