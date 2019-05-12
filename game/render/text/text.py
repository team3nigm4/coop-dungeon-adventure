from game.render.shape import shape
from game.util import matrix4f
from game.render.shader.shadermanager import ShaderManager as sm
from game.render.text.textmanager import TextManager as txm


class Text:

	def __init__(self, font):
		self.font = font
		self.color = [0, 0, 0, 1]
		self.numberLetter = 0
		self.vbo = []
		self.ebo = []
		self.text = ""
		self.size = 0
		self.centering = "center"

		self.shape = shape.Shape("text-hud", True)
		self.shape.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		self.shape.setReading([3, 2, 4])

		self.model = matrix4f.Matrix4f(True)
		self.model.matrix[3][0] -= 9
		self.model.matrix[3][1] -= 6

	def setFont(self, font):
		self.font = font
		if self.text != "":
			self.setText(self.text)

	def setCentering(self, newCentering):
		self.centering = newCentering

	def setColor(self, color):
		for col in range(4):
			if color[col] > 1:
				self.color[col] = color[col] /255
			else:
				self.color[col] = color[col]

		if self.text != "":
			for index in range(self.numberLetter):
				for i in range(4):
					for m in range(4):
						self.vbo[index * 36 + i * 9 + 5 + m] = self.color[m]

			self.shape.setVbo(self.vbo)

	def setPosition(self, position):
		self.model.matrix[3][0] = - 9 + position[0]
		self.model.matrix[3][1] = - 6 + position[1]

	def setSize(self, size):
		self.size = size
		if self.text != "":
			self.setText(self.text)

	def setText(self, text):
		self.ebo = []
		self.vbo = []

		self.vbo = txm.constructVbo(self.font, text, self.size, self.centering)
		self.text = text

		tempText = text
		self.numberLetter = len(tempText) - tempText.count("\n")

		for index in range(self.numberLetter):
			self.ebo.append(index * 4)
			self.ebo.append(index * 4 + 1)
			self.ebo.append(index * 4 + 3)
			self.ebo.append(index * 4 + 1)
			self.ebo.append(index * 4 + 2)
			self.ebo.append(index * 4 + 3)

		self.setColor(self.color)
		self.shape.setEbo(self.ebo)

	def setAll(self, text, size, position, color, centering):
		self.text = ""
		self.setCentering(centering)
		self.setPosition(position)
		self.setSize(size)
		self.setColor(color)
		self.setText(text)

	def display(self):
		sm.updateLink("text-hud", "model", self.model.matrix)

		txm.bind(self.font)
		self.shape.display()

	def unload(self):
		self.shape.unload()
