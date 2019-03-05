# Create a shape as you want and manage it

from game.render.shader.shadermanager import ShaderManager as sm

import OpenGL.GL as gl
import numpy


class Shape:
	def __init__(self, shaderID, useEBO):
		# Instance variables
		self.verticesNumber = None

		self.shaderId = shaderID

		self.useEBO = useEBO
		self.vao = gl.glGenVertexArrays(1)
		self.bind()
		self.vbo = gl.glGenBuffers(1)
		if useEBO:
			self.ebo = gl.glGenBuffers(1)
		self.unbind()


	def setVertices(self, vertices, info, indices=None):
		self.bind()
		if self.useEBO:
			if indices == None :
				print("(shape-setVertices) using EBO without providing indices(None)")
				exit(1)

			self.setEbo(indices)

		self.setVbo(vertices)
		vertices = numpy.array(vertices, dtype=numpy.float32)

		gl.glVertexAttribPointer(0, info[0], gl.GL_FLOAT, gl.GL_FALSE, sum(info) * vertices.itemsize,
								 gl.ctypes.c_void_p(0))
		gl.glEnableVertexAttribArray(0)
		for i in range(1, len(info)):
			gl.glVertexAttribPointer(i, info[i], gl.GL_FLOAT, gl.GL_FALSE, sum(info) * vertices.itemsize,
									 gl.ctypes.c_void_p(sum(info[:i]) * vertices.itemsize))
			gl.glEnableVertexAttribArray(i)


		if not self.useEBO:
			self.verticesNumber = int(len(vertices) / sum(info))

		self.unbind()

	def setVbo(self, vertices):
		self.bind()
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		vertices = numpy.array(vertices, dtype=numpy.float32)
		gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.itemsize * len(vertices), vertices, gl.GL_STATIC_DRAW)

	def setEbo(self, indices):
		self.bind()
		gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
		self.indicesNumber = len(indices)
		indices = numpy.array(indices, dtype=numpy.uint32)
		gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, gl.GL_STATIC_DRAW)

	def display(self):
		self.applyShader()
		self.bind()
		self.draw()
		self.unbind()

	def applyShader(self):
		sm.shaders[self.shaderId].use()

	def bind(self):
		gl.glBindVertexArray(self.vao)

	def unbind(self):
		gl.glBindVertexArray(0)

	def draw(self):
		if self.useEBO:
			gl.glDrawElements(gl.GL_TRIANGLES, self.indicesNumber, gl.GL_UNSIGNED_INT, None)
		else:
			gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.verticesNumber)

	def unload(self):
		gl.glDeleteBuffers(1, int(self.vbo))
		if self.useEBO:
			gl.glDeleteBuffers(1, int(self.ebo))
		gl.glDeleteVertexArrays(1, int(self.vao))

