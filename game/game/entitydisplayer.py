import pyrr

from game.render.shape import shape
from game.render.texture import texture
from game.render.shader.shadermanager import ShaderManager as sm

class EntityDisplayer:

	def __init__(self):
		self.size = None
		self.tex = None
		self.hotPoint = [0,0]

		self.hardSetImage([1,1], "no error (\"entityDisplayer\")", [0, 0])
		self.modelMtx = pyrr.Matrix44.identity()

	def display(self):
		sm.updateLink(sm.TEXTURE, "model", self.modelMtx)
		self.tex.bind()
		self.shape.display()

	def setImage(self, size, path, hotPoint):
		self.unload()
		self.hardSetImage(size, path, hotPoint)

	def hardSetImage(self, size, path, hotPoint):
		self.size = size
		self.hotPoint = hotPoint
		self.tex = texture.Texture(path)
		self.tex.load()
		self.hotPoint = 0

		size = self.size
		quad = [0 - hotPoint[0], 0 - hotPoint[1], 0.0, 0.0, 0.0,
				size[0] - hotPoint[0], 0 - hotPoint[1], 0.0, 1.0, 0.0,
				size[0] - hotPoint[0], size[1] - hotPoint[1], 0.0, 1.0, 1.0,
				0 - hotPoint[0], size[1] - hotPoint[1], 0.0, 0.0, 1.0]

		indices = [0, 1, 2,
				   2, 3, 0]

		self.shape = shape.Shape(0)
		self.shape.setEbo(indices)
		self.shape.setVertices(quad, [3, 2])

		self.modelMtx = pyrr.Matrix44.identity()

	def updateModel(self, newPos):
		self.modelMtx[3][0] = newPos[0]
		self.modelMtx[3][1] = newPos[1]

	def unload(self):
		self.tex.unload()
		self.shape.unload()