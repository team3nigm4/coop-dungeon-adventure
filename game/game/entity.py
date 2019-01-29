class Entity:
	ARGS_TYPE = 0
	ARGS_POSITION = 1

	def __init__(self, args):
		self.type = args[Entity.ARGS_TYPE]
		self.pos = args[Entity.ARGS_POSITION]

	def setPos(self, position):
		self.pos = position

	def update(self):
		pass

	def display(self):
		pass

	def unload(self):
		pass
