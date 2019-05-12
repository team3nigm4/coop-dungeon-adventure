# Class to instance a texture not influenced by the camera translations

from game.render.shape import shape
from game.render.shader.shadermanager import ShaderManager as sm
from game.util import matrix4f
from game.render.texture.texturemanager import TextureManager as tm


class GuiRenderer:
	def __init__(self):
		self.size = [0, 0]
		self.hotPoint = [0, 0]

		self.quad = [0, 0, 0.0, 	0.0, 0.0, 1.0,
				1, 0, 0.0, 	1.0, 0.0, 1.0,
				1, 1, 0.0, 	1.0, 1.0, 1.0,
				0, 1, 0.0, 	0.0, 1.0, 1.0]

		indices = [0, 1, 2,
				2, 3, 0]

		self.shape = shape.Shape("texture-hud", True)
		self.shape.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		self.shape.setEbo(indices)
		self.shape.setVbo(self.quad)
		self.shape.setReading([3, 2, 1])

		self.setKey("error")
		self.model = matrix4f.Matrix4f(True)

	def display(self):
		sm.updateLink("texture-hud", "model", self.model.matrix)
		tm.bind(self.texKey)
		self.shape.display()

	# Define an image with this size, the image will be centered in the renderer's position
	def setImage(self, size, key):
		self.size = size
		self.hotPoint = [size[0] / 2, size[1] /2]
		hotPoint = self.hotPoint
		self.setKey(key)

		size = self.size
		self.quad = [0 - hotPoint[0], 0 - hotPoint[1], 0.0, 0.0, 0.0, 1.0,
				size[0] - hotPoint[0], 0 - hotPoint[1], 0.0, 1.0, 0.0, 1.0,
				size[0] - hotPoint[0], size[1] - hotPoint[1], 0.0, 1.0, 1.0, 1.0,
				0 - hotPoint[0], size[1] - hotPoint[1], 0.0, 0.0, 1.0, 1.0]

		self.shape.setVbo(self.quad)

	def setOpacity(self, opacity):
		for i in range(4):
			self.quad[i * 6 + 5] = opacity
		self.shape.setVbo(self.quad)

	def setKey(self, key):
		self.texKey = tm.key(key)

	# Update the position of the renderer
	def updateModel(self, newPos):
		self.model.matrix[3][0] = newPos[0] - 9
		self.model.matrix[3][1] = newPos[1] - 6

	def unload(self):
		self.shape.unload()
