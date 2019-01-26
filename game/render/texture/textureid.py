# Contains the path and the id of a texture


class TextureId:
	def __init__(self, path):
		# Create attributes
		self.id = None
		self.path = None

		self.setId(id)
		self.setPath(path)

	def getPath(self):
		return self.path

	def setPath(self, newPath):
		self.path = newPath	

	def getId(self):
		return self.id

	def setId(self, newId):
		self.id = newId
