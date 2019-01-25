import OpenGL.GL as gl

def glUniform(shader, name, value1):
	shader.use()
	gl.glUniform1f(shader.getLink(name), value1)

def glUniform(shader, name, value1, value2):
	shader.use()
	gl.glUniform2f(shader.getLink(name), value1, value2)

def glUniform(shader, name, value1, value2, value3):
	shader.use()
	gl.glUniform3f(shader.getLink(name), value1, value2, value3)

def glUniform(shader, name, value1, value2, value3, value4):
	shader.use()
	gl.glUniform4f(shader.getLink(name), value1, value2, value3, value4)

def glUniformv(shader, name, value1):
	shader.use()
	gl.glUniformMatrix4fv(shader.getLink(name),1,  gl.GL_FALSE, value1)