# Manages all textures to know which ones are loaded

from game.render.texture import texture
from game.util.logger import Logger


class TextureManager:
	def __init__(self):
		self.texIds = []
		self.error = None

	def init(self):
		self.error = texture.Texture("error.png")
		self.error.load()

	def add(self, texId):
		self.texIds.append(texId)

	def remove(self, texId):
		self.texIds.remove(texId)

	def state(self):
		Logger.info("TEXTURE MANAGER", "Textures currently loaded :")
		print("=" * 45)
		for tex in self.texIds:
			print("Texture " + str(tex.getId()) + ", from " + tex.getPath())
		print("=" * 45)

	def endState(self):
		if len(self.texIds) > 0:
			Logger.error("TEXTURE MANAGER", "Error at the end of the program ->")
			self.state()
		else:
			Logger.info("TEXTURE MANAGER", "No remaining textures")
