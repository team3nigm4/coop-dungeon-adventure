

class EntityManager:
	PLAYER_1 = 0
	PLAYER_2 = 1

	entities = []
	entitiesCol = []

	@staticmethod
	def init():
		pass

	@staticmethod
	def update():
		for e in EntityManager.entities:
			e.update()

	@staticmethod
	def display():
		for e in EntityManager.entities:
			e.display()

	@staticmethod
	def add(entity):
		place = EntityManager.checkPlace()
		entity.setId(place)

		if place == len(EntityManager.entities):
			EntityManager.entities.append(entity)
		else:
			EntityManager.entities[place] = entity

	@staticmethod
	def remove(id):
		EntityManager.entities[id].unload()
		if id == len(EntityManager.entities)-1:
			EntityManager.remove(id)
		else:
			from game.game.entityclass import entity
			EntityManager.entities[id] = entity.Entity([0, [0, 0]])
			entity.setId(-1)

	@staticmethod
	def clear():
		size = len(EntityManager.entities)
		if size > 2:
			for i in range(2, size):
				EntityManager.entities[2].unload()
				EntityManager.entities.remove(2)

	@staticmethod
	def unload():
		print("\nUnload EntityManager :")
		for e in EntityManager.entities:
			e.unload()
		print("\n")

	@staticmethod
	def checkPlace():
		for i in range(0, len(EntityManager.entities)):
			if EntityManager.entities[i].id == -1:
				return i
		return len(EntityManager.entities)

	@staticmethod
	def addToTest(id):
		EntityManager.entitiesCol.append(id)

	@staticmethod
	def removeToTest(id):
		EntityManager.entitiesCol.remove(id)
