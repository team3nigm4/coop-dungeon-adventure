# Class to create a button with its text and its action

from game.render.shape import guirenderer
from game.inputs.mousemanager import MouseManager
from game.render.text import text

class Button:
	def __init__(self, pos, size, tex, function):
		self.pos = [0,0]
		self.size = size
		self.size[0] *= 1.1
		self.size[1] *= 1.1
		self.renderer = guirenderer.GuiRenderer()
		self.renderer.setImage(self.size, "button-unhover")

		self.hover = True

		self.text = text.Text("pixel1")
		self.isUnhover()

		self.text.setText(tex)
		self.func = function

		self.setPos(pos)

	def update(self):
		mouse = MouseManager.mousePosRelative
		if self.pos[0] - self.size[0] / 2 < mouse[0]  < self.pos[0] + self.size[0] / 2:
			if self.pos[1] - self.size[1] / 2 < mouse[1] < self.pos[1] + self.size[1] / 2:
				self.isHover()
				if MouseManager.buttonPressed(0):
					self.func()
			else:
				self.isUnhover()
		else:
			self.isUnhover()

	def isUnhover(self):
		if self.hover:
			self.hover = False
			self.size[0] /= 1.1
			self.size[1] /= 1.1
			self.text.setColor([0.8, 0.8, 0.8, 1])
			self.text.setSize(self.size[0] / 8)
			self.renderer.setImage(self.size, "button-unhover")

	def isHover(self):
		if not self.hover:
			self.hover = True
			self.size[0] *= 1.1
			self.size[1] *= 1.1
			self.text.setColor([1, 1, 1, 1])
			self.text.setSize(self.size[0] / 8)
			self.renderer.setImage(self.size, "button-hover")

	def display(self):
		self.renderer.display()
		self.text.display()

	def setPos(self, pos):
		# Re set the position of the button, and to its renderer and its text
		self.pos = pos
		self.renderer.updateModel(pos)
		self.text.setPosition(self.pos)

	def unload(self):
		self.renderer.unload()
