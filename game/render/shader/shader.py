import OpenGL.GL as gl

class Shader:
	PATH = "game/resources/shader/"
	def __init__(self, vertexPath, fragmentPath):
		self.vertexPath = vertexPath
		self.fragmentPath = fragmentPath
		self.shaderId = 1
		self.links = {}

	def load(self):
		shaderId  = gl.glCreateProgram()
		vertexId = gl.glCreateShader(gl.GL_VERTEX_SHADER)
		fragmentId = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

		vertexFile = open(Shader.PATH + self.vertexPath, 'r') 
		vertexCode = vertexFile.read()       
		vertexFile.close()                                 

		fragmentfile = open(Shader.PATH + self.fragmentPath, 'r')
		fragmentCode = fragmentfile.read()
		fragmentfile.close()

		gl.glShaderSource(vertexId, vertexCode)
		gl.glShaderSource(fragmentId, fragmentCode)

		gl.glCompileShader(vertexId)
		if not gl.glGetShaderiv(vertexId, gl.GL_COMPILE_STATUS):
			error = gl.glGetShaderInfoLog(vertexId).decode()
			print(error)
			raise RuntimeError("Vertex shader compilation error")

		gl.glCompileShader(fragmentId)
		if not gl.glGetShaderiv(fragmentId, gl.GL_COMPILE_STATUS):
			error = gl.glGetShaderInfoLog(fragmentId).decode()
			print(error)
			raise RuntimeError("Fragment shader compilation error")

		gl.glAttachShader(shaderId, vertexId)
		gl.glAttachShader(shaderId, fragmentId)
		gl.glLinkProgram(shaderId)
		if not gl.glGetProgramiv(shaderId, gl.GL_LINK_STATUS):
			print(gl.glGetProgramInfoLog(shaderId))
			raise RuntimeError('Linking error')

		gl.glDetachShader(shaderId, vertexId)
		gl.glDetachShader(shaderId, fragmentId)
		gl.glDeleteShader(vertexId)
		gl.glDeleteShader(fragmentId)
		self.shaderId = shaderId


	def addLink(self, valueName):
		self.links[valueName] = gl.glGetUniformLocation(self.shaderId, valueName)

	def getLink(self, valueName):
		return self.links.get(valueName)

	def use(self):
		gl.glUseProgram(self.shaderId)

	def getId(self):
		return self.shaderId

	def unload(self):
		gl.glDeleteProgram(self.shaderId)	