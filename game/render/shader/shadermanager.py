# Manager every shader using by the game

from game.render.shader import gluniforms as glU
from game.render.shader import shader
from game.screen import gamemanager as gm
from game.util import matrix4f
import json


class ShaderManager:
	TEXTURE = 0
	BOX = 1

	shaders = {}
	reloading = {}

	@staticmethod
	def init():
		# Load the characteristics files
		info = json.load(open("game/resources/shader/shaders.json"))

		for e in info["reloading"]:
			attribute = info["reloading"][e]

			if attribute == "camView":
				ShaderManager.addReloading(e, gm.GameManager.cam.getView())

		# Load each shader registered
		for shad in info["shaders"]:
			infos = info["shaders"][shad].copy()

			ShaderManager.shaders[shad] = shader.Shader(infos["files"][0],
														infos["files"][1])
			ShaderManager.shaders[shad].load()
			ShaderManager.shaders[shad].use()
			ShaderManager.shaders[shad].addLink("projection")
			glU.glUniformv(ShaderManager.shaders[shad], "projection", gm.GameManager.cam.getProjection())
			ShaderManager.shaders[shad].addLink("view")
			ShaderManager.shaders[shad].addLink("model")

			for reload in infos["mode"]:
				if reload == "camView":
					ShaderManager.addToReload("view", shad)
				elif reload == "static":
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
