# Manages all textures to know which ones are loaded

from game.render.texture import texture


class TextureManager:
	def __init__(self):
		self.texIds = []
		self.error = "null"

	def init(self):
		self.error = texture.Texture("game/resources/textures/error.png")
		self.error.load()

	def add(self, texId):
		self.texIds.append(texId)

	def remove(self, texId):
		self.texIds.remove(texId)

	def state(self):
		print("Textures currently loaded :")
		print("=" * 24)
		for tex in self.texIds:
			print("Texture " + str(tex.getId()) + ", from " + tex.getPath())
		print("=" * 24)

	def endState(self):
		if len(self.texIds) > 0:
			print("\nError at the end of the program ->")
			self.state()
		else:
			print("\nNo remaining textures\n")