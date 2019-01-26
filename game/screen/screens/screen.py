# Parent class of every class screen


class Screen:
	def __init__(self):
		self.screenState = None

	def setScreen(self, newScreen):
		self.screenState = newScreen
