# Manager every shader using by the game

from game.render.shader import gluniforms as glU
from game.render.shader import shader
from game.screen import gamemanager as gm
from game.util import matrix4f


class ShaderManager:
	TEXTURE = 0
	BOX = 1

	shaders = {}
	reloading = {}

	@staticmethod
	def init():
		ShaderManager.shaders["box"] = shader.Shader("boxVert.glsl", "boxFrag.glsl")
		ShaderManager.shaders["texture"] = shader.Shader("texVert.glsl", "texFrag.glsl")
		ShaderManager.shaders["hud"] = shader.Shader("texHudVert.glsl", "texHudFrag.glsl")

		for e in ShaderManager.shaders:
			ShaderManager.shaders[e].load()
			ShaderManager.shaders[e].use()
			ShaderManager.shaders[e].addLink("projection")
			glU.glUniformv(ShaderManager.shaders[e], "projection", gm.GameManager.cam.getProjection())

			ShaderManager.shaders[e].addLink("view")
			ShaderManager.shaders[e].addLink("model")

		ShaderManager.addReloading("view", gm.GameManager.cam.getView())

		ShaderManager.addToReload("view", "texture")
		ShaderManager.addToReload("view", "box")

		matrix = matrix4f.Matrix4f(True)
		matrix.matrix[3][2] = -8.572
		glU.glUniformv(ShaderManager.shaders["hud"], "view", matrix.matrix)

		ShaderManager.dispose()

	@staticmethod
	def updateLink(key, link, value):
		ShaderManager.shaders[key].use()
		glU.glUniformv(ShaderManager.shaders[key], link, value)

	@staticmethod
	def updateLinkf(key, link, value):
		ShaderManager.shaders[key].use()
		glU.glUniformf(ShaderManager.shaders[key], link, value)

	@staticmethod
	def addToReload(key, shader):
		ShaderManager.reloading[key][0].append(shader)

	@staticmethod
	# value must to be a function
	def addReloading(key, value):
		ShaderManager.reloading[key] = [[], value]

	@staticmethod
	def dispose():
		for reload in ShaderManager.reloading:
			for shader in ShaderManager.reloading[reload][0]:
				ShaderManager.updateLink(shader, reload, ShaderManager.reloading[reload][1])

	@staticmethod
	def unload():
		for i in ShaderManager.shaders:
			ShaderManager.shaders[i].unload()
