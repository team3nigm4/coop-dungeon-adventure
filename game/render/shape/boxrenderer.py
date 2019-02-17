import pyrr

from game.render.shape import shape
from game.render.shader.shadermanager import ShaderManager as sm


class BoxRenderer:

	def __init__(self, size, color):
		self.size = size
		self.color = color

		quad = [0, 0, 0.0, 							self.color[0], self.color[1], self.color[2], self.color[3],
				self.size[0], 0, 0.0, 				self.color[0], self.color[1], self.color[2], self.color[3],
				self.size[0], self.size[1], 0.0, 	self.color[0], self.color[1], self.color[2], self.color[3],
				0, self.size[1], 0.0, 				self.color[0], self.color[1], self.color[2], self.color[3]]

		indices = [0, 1, 2,
				2, 3, 0]

		self.shape = shape.Shape(1, True)
		self.shape.setVertices(quad, [3, 2], indices)

		self.modelMtx = pyrr.Matrix44.identity()

	def display(self):
		sm.updateLink(sm.TEXTURE, "model", self.modelMtx)
		self.shape.display()

	def setAttributes(self, size, color):
		self.color = color
		self.size = size
		quad = [0, 0, 0.0, 							self.color[0], self.color[1], self.color[2], self.color[3],
				self.size[0], 0, 0.0, 				self.color[0], self.color[1], self.color[2], self.color[3],
				self.size[0], self.size[1], 0.0, 	self.color[0], self.color[1], self.color[2], self.color[3],
				0, self.size[1], 0.0, 				self.color[0], self.color[1], self.color[2], self.color[3]]


		self.shape.resetVBO(quad)

	def updateModel(self, newPos):
		self.modelMtx[3][0] = newPos[0]
		self.modelMtx[3][1] = newPos[1]

	def unload(self):
		self.shape.unload()
