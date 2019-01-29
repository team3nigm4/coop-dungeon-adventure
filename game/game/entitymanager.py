from game.game import entity


class EntityManager:
	PLAYER_1 = 0
	PLAYER_2 = 0

	entities = []

	@staticmethod
	def init():
		pass

	@staticmethod
	def addNew(args):
		EntityManager.entities.append(entity.Entity(args))

	@staticmethod
	def add(entity):
		EntityManager.entities.append(entity)

	@staticmethod
	def update():
		for e in EntityManager.entities:
			e.update()

	@staticmethod
	def display():
		for e in EntityManager.entities:
			e.display()

	@staticmethod
	def clear():
		size = len(EntityManager.entities)
		if size > 2:
			for i in range(3, size):
				EntityManager.entities.remove(3)

	@staticmethod
	def unload():
		print("\nUnload EntityManager :")
		for e in EntityManager.entities:
			e.unload()
		print("\n")
