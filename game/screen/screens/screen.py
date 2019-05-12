# Parent class of every screen class 


class Screen:
	def __init__(self):
		pass
	
	def init(self):
		pass

	def setScreen(self, newScreen, args):
		from game.screen.gamemanager import GameManager
		
		GameManager.setCurrentScreen(newScreen, args)
