# Class to display the main game menu

from game.inputs.inputmanager import InputManager as im
from game.screen.screens import screen
from game.render.text import text
from game.render.gui import button
from game.render.shape import guirenderer
from game.screen import gamemanager


class MenuScreen(screen.Screen):

	def __init__(self, info):
		super().__init__()
		
		self.copyleft = text.Text("pixel1")
		self.copyleft.setAll("(C) 2019 Maxence, Alexandre & Baptiste" + " " * 29 + "v.0.1", 0.4, [0, 0], [1,1,1,1], "down-left")

		self.credits = text.Text("pixel1")
		self.credits.setAll("Maxence Bazin\nAlexandre Boin\nBaptiste Aleci",  0.45,  [9, 4.7], [1,1,1,1], "")

		self.background = guirenderer.GuiRenderer()
		self.background.setImage([18, 12], "background")
		
		self.screenTitle = guirenderer.GuiRenderer()
		self.screenTitle.setImage([18, 12], "screentitle")

		self.showCredits = False

		def gameLocal():
			from game.screen import gamemanager
			gamemanager.GameManager.setCurrentScreen("gamescreen", [False])

		def gameMulti():
			from game.screen import gamemanager
			gamemanager.GameManager.setCurrentScreen("gamescreen", [True])

		def gameQuit():
			from game.main.window import Window
			Window.exit()

		def toggleCredits(): self.showCredits ^= True

		self.playLocal = button.Button([9, 5.9], [5, 1], "Local", gameLocal)

		self.playMulti = button.Button([9, 4.4], [5, 1], "Mutltijoueur", gameMulti)
		
		self.showCreditsBtn = button.Button([7.7, 3.3], [2.45, 0.6], "Crédits", toggleCredits)

		self.hideCreditsBtn = button.Button([7.7, 3.3], [2.45, 0.6], "< Retour", toggleCredits)
		
		self.quit = button.Button([10.3, 3.3], [2.45, 0.6], "Quitter", gameQuit)

	def update(self):
			# Exit test
			if im.inputPressed(im.ESCAPE):
				from game.main.window import Window
				Window.exit()
				
			# Update buttons
			self.playLocal.update()
			self.playMulti.update()
			if self.showCredits:
				self.hideCreditsBtn.update()
			else:
				self.showCreditsBtn.update()
			self.quit.update()

	def display(self):
		self.background.display()
		self.screenTitle.display()
		self.copyleft.display()
		self.quit.display()
		
		if self.showCredits:
			self.credits.display()
			self.hideCreditsBtn.display()
		else:
			self.playLocal.display()
			self.playMulti.display()
			self.showCreditsBtn.display()

	def unload(self):
		self.background.unload()
		self.screenTitle.unload()
		self.copyleft.unload()
		self.playLocal.unload()
		self.playMulti.unload()
		self.showCreditsBtn.unload()
		self.hideCreditsBtn.unload()
		self.quit.unload()

