# Create a shape as you want and manage it

from game.render.shader.shadermanager import ShaderManager as sm

import OpenGL.GL as gl
import numpy


class Shape:
	STATIC_STORE = gl.GL_STATIC_DRAW
	DYNAMIC_STORE = gl.GL_DYNAMIC_DRAW
	STREAM_STORE = gl.GL_STREAM_DRAW

	def __init__(self, shaderID, useEBO):
		# Instance variables
		self.verticesNumber = None

		self.shaderId = shaderID

		self.vao = gl.glGenVertexArrays(1)
		self.bind()
		self.vbo = gl.glGenBuffers(1)
		self.ebo = 0
		self.useEBO = useEBO
		self.setUseEbo(useEBO)
		self.unbind()

	def setUseEbo(self, state):
		if self.useEBO:
			gl.glDeleteBuffers(1, int(self.ebo))

		self.useEBO = state

		if self.useEBO:
			self.ebo = gl.glGenBuffers(1)

	def setStorage(self, vboStorage, eboStorage):
		self.vboStorage = vboStorage
		self.eboStorage = eboStorage

	def setReading(self, info):
		self.bind()
		self.info = info
		self.setVbo([0.0 for i in range(sum(info))])
		numpySize = numpy.array([0.0], dtype=numpy.float32).itemsize

		gl.glVertexAttribPointer(0, info[0], gl.GL_FLOAT, gl.GL_FALSE, sum(info) * numpySize,
								 gl.ctypes.c_void_p(0))
		gl.glEnableVertexAttribArray(0)
		for i in range(1, len(info)):
			gl.glVertexAttribPointer(i, info[i], gl.GL_FLOAT, gl.GL_FALSE, sum(info) * numpySize,
									 gl.ctypes.c_void_p(sum(info[:i]) * numpySize))
			gl.glEnableVertexAttribArray(i)

		self.unbind()

	def setVbo(self, vertices):
		self.bind()
		if not self.useEBO:
			self.verticesNumber = int(len(vertices) / sum(self.info))
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		vertices = numpy.array(vertices, dtype=numpy.float32)

		gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.itemsize * len(vertices), vertices, self.vboStorage)

	def setEbo(self, indices):
		if not self.useEBO:
			print("(shape-setEbo) providing EBO without using EBO")
			return EOFError
		self.bind()
		gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
		self.indicesNumber = len(indices)
		indices = numpy.array(indices, dtype=numpy.uint32)
		gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, self.eboStorage)

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

