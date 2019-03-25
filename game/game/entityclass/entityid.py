class EntityId:
	def __init__(self):
		self.defaultId()
		
	def setId(self, newId):
		if newId >= 0:
			self.id = newId

	def defaultId(self):
		self.id = -1

	def getId(self):
		return self.id
