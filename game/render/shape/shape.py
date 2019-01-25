from game.render.shader import shader as shad
from game.render.shader import gluniforms as glU
from game.screen import gamemanager as gameManager

import OpenGL.GL as gl
import numpy
import pyrr

class Shape:
	def __init__(self, vertexPath, fragmentPath):
		self.shader = shad.Shader(vertexPath, fragmentPath)
		self.shader.load()
		self.load()

	def load(self):
		self.shader.addLink("projection")
		glU.glUniformv(self.shader,"projection",  gameManager.GameManager.cam.getProjection())
		self.shader.addLink("view")
		view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))

		glU.glUniformv(self.shader, "view", gameManager.GameManager.cam.getView())

		self.vbo = gl.glGenBuffers(1)

	def setVertices(self, vertices, info):
		self.bind()
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		vertices = numpy.array(vertices, dtype = numpy.float32)
		gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.itemsize * len(vertices), vertices, gl.GL_STATIC_DRAW)

		for i in range (0, len(info)):
			gl.glVertexAttribPointer(i, info[i], gl.GL_FLOAT, gl.GL_FALSE, len(vertices), gl.ctypes.c_void_p(i*12))
			gl.glEnableVertexAttribArray(i)
     

	def setEbo(self, indices):
		self.bind()
		self.ebo = gl.glGenBuffers(1)
		self.indLenght = len(indices)
		gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
		indices = numpy.array(indices, dtype= numpy.uint32)
		gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, gl.GL_STATIC_DRAW)

	def defaultEbo(self, size):
		setEbo([i for i in np.arange(0, size, 1)])

	def display(self):
		self.applyShader()
		self.bind()
		self.view()
		self.draw()

	def bind(self):
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

	def draw(self):
		gl.glDrawElements(gl.GL_TRIANGLES, self.indLenght, gl.GL_UNSIGNED_INT, None)

	def applyShader(self):
		self.shader.use()

	def view(self):
		glU.glUniformv(self.shader, "view", gameManager.GameManager.cam.getView())

	def unload(self):
		gl.glDeleteBuffers(self.vbo, 1)
		self.shader.unload()