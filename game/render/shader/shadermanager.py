# Manager every shader using by the game

from game.render.shader import gluniforms as glU
from game.render.shader import shader
from game.screen import gamemanager as gm


class ShaderManager:
	TEXTURE = 0
	BOX = 1

	shaders = {}
	reloading = {}

	@staticmethod
	def init():
		ShaderManager.shaders["box"] = shader.Shader("boxVert.glsl", "boxFrag.glsl")
		ShaderManager.shaders["box"].load()
		ShaderManager.shaders["box"].use()

		ShaderManager.shaders["box"].addLink("projection")
		glU.glUniformv(ShaderManager.shaders["box"], "projection", gm.GameManager.cam.getProjection())

		ShaderManager.shaders["box"].addLink("view")
		ShaderManager.shaders["box"].addLink("model")

		# Box shader
		ShaderManager.shaders["texture"] = shader.Shader("texVert.glsl", "texFrag.glsl")
		ShaderManager.shaders["texture"].load()
		ShaderManager.shaders["texture"].use()

		ShaderManager.shaders["texture"].addLink("projection")
		glU.glUniformv(ShaderManager.shaders["texture"], "projection", gm.GameManager.cam.getProjection())

		ShaderManager.shaders["texture"].addLink("view")
		ShaderManager.shaders["texture"].addLink("model")

		ShaderManager.addReloading("view", gm.GameManager.cam.getView())
		ShaderManager.addToReload("view", "texture")
		ShaderManager.addToReload("view", "box")

		ShaderManager.dispose()

	@staticmethod
	def updateLink(key, link, value):
		ShaderManager.shaders[key].use()
		glU.glUniformv(ShaderManager.shaders[key], link, value)

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
