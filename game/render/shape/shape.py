# Create a shape as you want and manage it

from game.render.shader.shadermanager import ShaderManager as sm

import OpenGL.GL as gl
import numpy


class Shape:
	def __init__(self, shaderID):
		# Instance variables
		self.ebo = None
		self.vbo = None
		self.verticesNumber = None
		self.shaderId = shaderID

		self.load()

	def load(self):
		self.vao = gl.glGenVertexArrays(1)
		self.bind()
		self.vbo = gl.glGenBuffers(1)

	def setVertices(self, vertices, info):
		self.bind()
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		vertices = numpy.array(vertices, dtype=numpy.float32)
		gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.itemsize * len(vertices), vertices, gl.GL_STATIC_DRAW)

		for i in range(0, len(info)):
			gl.glVertexAttribPointer(i, info[i], gl.GL_FLOAT, gl.GL_FALSE, len(vertices), gl.ctypes.c_void_p(i*12))
			gl.glEnableVertexAttribArray(i)

	def setEbo(self, indices):
		self.bind()
		self.ebo = gl.glGenBuffers(1)
		self.verticesNumber = len(indices)

		indices = numpy.array(indices, dtype=numpy.uint32)

		gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
		gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, gl.GL_STATIC_DRAW)

	def defaultEbo(self, size):
		self.setEbo([i for i in numpy.arange(0, size, 1)])

	def display(self):
		self.applyShader()
		self.bind()
		self.draw()

	def applyShader(self):
		sm.shaders[self.shaderId].use()

	def bind(self):
		gl.glBindVertexArray(self.vao)

	def draw(self):
		gl.glDrawElements(gl.GL_TRIANGLES, self.verticesNumber, gl.GL_UNSIGNED_INT, None)

	def unload(self):
		print("vao : ", self.vao, ", vbo : ", self.vbo, ", ebo : ", self.ebo)
		gl.glDeleteVertexArrays(self.vao, 1)
		gl.glDeleteBuffers(self.vbo, 1)
		gl.glDeleteBuffers(self.ebo, 1)

