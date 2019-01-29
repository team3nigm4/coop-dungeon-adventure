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
			print("vao ", self.vao, ", ebo", self.ebo, ", vbo", self.vbo)
		self.unbind()


	def setVertices(self, vertices, info, indices=None):
		self.bind()
		if self.useEBO:
			if indices == None :
				print("(shape-setVertices) using EBO without providing indices(None)")
				exit(1)

			self.verticesNumber = len(indices)

			indices = numpy.array(indices, dtype=numpy.uint32)

			gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
			gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, gl.GL_STATIC_DRAW)

		self.resetVBO(vertices)

		for i in range(0, len(info)):
			gl.glVertexAttribPointer(i, info[i], gl.GL_FLOAT, gl.GL_FALSE, len(vertices), gl.ctypes.c_void_p(i*12))
			gl.glEnableVertexAttribArray(i)

		if not self.useEBO:
			self.verticesNumber = len(vertices) / sum(info)

		self.unbind()

	def resetVBO(self, vertices):
		self.bind()
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		vertices = numpy.array(vertices, dtype=numpy.float32)
		gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.itemsize * len(vertices), vertices, gl.GL_STATIC_DRAW)

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
			gl.glDrawElements(gl.GL_TRIANGLES, self.verticesNumber, gl.GL_UNSIGNED_INT, None)
		else:
			gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.verticesNumber)

	def unload(self):
		gl.glDeleteBuffers(self.vbo, 1)
		if self.useEBO:
			gl.glDeleteBuffers(self.ebo, 1)
		gl.glDeleteVertexArrays(self.vao, 1)

