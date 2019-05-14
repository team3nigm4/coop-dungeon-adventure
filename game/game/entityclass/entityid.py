# Class to contain the id of an entity, the advantage is that class is mutable
# We don't have to redefine this id of the entity in managers if this id change for some reasons

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
