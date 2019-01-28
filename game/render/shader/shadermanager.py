# Manager every shader using by the game

from game.render.shader import gluniforms as glU
from game.render.shader import shader
from game.screen import gamemanager as gm


class ShaderManager:
	TEXTURE = 0

	shaders = None

	@staticmethod
	def init():
		ShaderManager.shaders = []
		ShaderManager.shaders.append(shader.Shader("texVert.glsl", "texFrag.glsl"))
		ShaderManager.shaders[0].load()

		ShaderManager.shaders[0].addLink("projection")
		glU.glUniformv(ShaderManager.shaders[0], "projection", gm.GameManager.cam.getProjection())

		ShaderManager.shaders[0].addLink("view")
		ShaderManager.shaders[0].addLink("model")

	@staticmethod
	def updateLink(num, link, value):
		glU.glUniformv(ShaderManager.shaders[num], link, value)

	@staticmethod
	def unload():
		for i in ShaderManager.shaders:
			i.unload()
