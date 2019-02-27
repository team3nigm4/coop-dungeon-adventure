import pyrr

from game.render.shape import shape
from game.render.shader.shadermanager import ShaderManager as sm


class BoxRenderer:
	def __init__(self, size, color):
		self.size = size
		self.color = color

		quad = [0, 0, 0.0, 						self.color[0], self.color[1], self.color[2], self.color[3],
				size[0], 0, 0.0, 				self.color[0], self.color[1], self.color[2], self.color[3],
				size[0], size[1], 0.0, 			self.color[0], self.color[1], self.color[2], self.color[3],
				0, size[1], 0.0, 				self.color[0], self.color[1], self.color[2], self.color[3]]

		indices = [0, 1, 2,
				2, 3, 0]

		self.shape = shape.Shape("box", True)
		self.shape.setVertices(quad, [3, 4], indices)

		self.modelMtx = pyrr.Matrix44.identity()

	def display(self):
		sm.updateLink("box", "model", self.modelMtx)
		self.shape.display()

	def setAttributes(self, size, color):
		self.color = color
		self.size = size
		quad = [0, 0, 0.0, 						self.color[0], self.color[1], self.color[2], self.color[3],
				size[0], 0, 0.0, 				self.color[0], self.color[1], self.color[2], self.color[3],
				size[0], size[1], 0.0, 			self.color[0], self.color[1], self.color[2], self.color[3],
				0, size[1], 0.0, 				self.color[0], self.color[1], self.color[2], self.color[3]]


		self.shape.resetVBO(quad)

	def updateModel(self, newPos):
		self.modelMtx[3][0] = newPos[0] - self.size[0] / 2
		self.modelMtx[3][1] = newPos[1] - self.size[1] / 2

	def unload(self):
		self.shape.unload()
