from game.render.shape import shape
from game.render.shader.shadermanager import ShaderManager as sm
from game.util import matrix4f
from game.render.texture.texturemanager import TextureManager as tm


class EntityRenderer:

	def __init__(self):
		self.size = [0, 0]
		self.hotPoint = [0, 0]

		quad = [0, 0, 0.0, 	0.0, 0.0,
				1, 0, 0.0, 	1.0, 0.0,
				1, 1, 0.0, 	1.0, 1.0,
				0, 1, 0.0, 	0.0, 1.0]

		indices = [0, 1, 2,
				2, 3, 0]

		self.shape = shape.Shape("texture", True)
		self.shape.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		self.shape.setEbo(indices)
		self.shape.setVbo(quad)
		self.shape.setReading([3, 2])

		self.texKey = "error"
		self.model = matrix4f.Matrix4f(True)

	def display(self):
		sm.updateLink("texture", "model", self.model.matrix)
		tm.bind(self.texKey)
		self.shape.display()

	def setImage(self, size, key, hotPoint):
		self.size = size
		self.hotPoint = hotPoint
		self.texKey = tm.isKey(key)
		self.texKey = key

		size = self.size
		quad = [0 - hotPoint[0], 0 - hotPoint[1], 0.0, 0.0, 0.0,
				size[0] - hotPoint[0], 0 - hotPoint[1], 0.0, 1.0, 0.0,
				size[0] - hotPoint[0], size[1] - hotPoint[1], 0.0, 1.0, 1.0,
				0 - hotPoint[0], size[1] - hotPoint[1], 0.0, 0.0, 1.0]

		self.shape.setVbo(quad)

	def updateModel(self, newPos):
		self.model.matrix[3][0] = newPos[0]
		self.model.matrix[3][1] = newPos[1]

	def unload(self):
		self.shape.unload()
