# Manage every entity of the game

class EntityManager:
	PLAYER_1 = 0
	PLAYER_2 = 1

	entities = []
	entitiesCol = []

	len = 0

	@staticmethod
	def init():
		EntityManager.len = 0

	@staticmethod
	def update():

		for e in EntityManager.entities:
			e.update()

	@staticmethod
	def display():
		e = EntityManager.len - 1
		while e >= 0:
			EntityManager.entities[e].display()
			e -= 1

	@staticmethod
	def collision():
		for i in range(0, len(EntityManager.entitiesCol) - 1):
			for a in range(1 + i, len(EntityManager.entitiesCol)):
				if EntityManager.canCol(EntityManager.entities[EntityManager.entitiesCol[i]],
										EntityManager.entities[EntityManager.entitiesCol[a]]):
					EntityManager.testCollision(EntityManager.entities[EntityManager.entitiesCol[i]],
												EntityManager.entities[EntityManager.entitiesCol[a]])

	@staticmethod
	# Collision rect aabb
	def testCollision(ent1, ent2):
		if ent2.pos[0] - ent2.halfColSize[0] >= ent1.pos[0] + ent1.halfColSize[0] or \
				ent2.pos[0] + ent2.halfColSize[0] <= ent1.pos[0] - ent1.halfColSize[0] or \
				ent2.pos[1] - ent2.halfColSize[1] >= ent1.halfColSize[1] + ent1.pos[1] or \
				ent2.pos[1] + ent2.halfColSize[1] <= ent1.pos[1] - ent1.halfColSize[1]:

			pass
		else:
			# print("Collision with :", ent1.type, "(" + str(ent1.id) + ") and", ent2.type + "(" + str(ent2.id) + ")")
			for i in ent1.attributes:
				if ent2.attributes[i] == 2 and ent1.attributes[i] > 0:
					ent2.collision(ent1)
				if ent1.attributes[i] == 2 and ent2.attributes[i] > 0:
					ent1.collision(ent2)

	@staticmethod
	def canCol(ent1, ent2):
		for i in ent1.attributes:
			if ent1.attributes[i] > 0:
				if ent2.attributes[i] > 0:
					return True

		return False

	@staticmethod
	def add(entity):

		if entity.id == EntityManager.len:
			EntityManager.entities.append(entity)
		else:
			EntityManager.entities[entity.id] = entity

		EntityManager.len = len(EntityManager.entities)

	@staticmethod
	def remove(id):
		# Unload the entity
		EntityManager.entities[id].unload()

		if id == len(EntityManager.entities) - 1:
			del EntityManager.entities[id]
			EntityManager.entities.remove(id)
		else:
			from game.game.entityclass import entity
			EntityManager.entities[id] = entity.Entity([0, [0, 0]])
			EntityManager.entities[id].setId(-1)

		EntityManager.len = len(EntityManager.entities)

	@staticmethod
	def clear():
		# Delete h
		if EntityManager.len > 1:
			for i in range(1, EntityManager.len):
				EntityManager.entities[1].unload()
				EntityManager.entities.remove(EntityManager.entities[1])

		EntityManager.entitiesCol = [0]
		EntityManager.len = len(EntityManager.entities)

	@staticmethod
	def unload():
		print("\nUnload EntityManager :")
		for e in EntityManager.entities:
			e.unload()
		print("\n")

	@staticmethod
	def checkPlace():
		for i in range(0, EntityManager.len):
			if EntityManager.entities[i].id == -1:
				return i
		return len(EntityManager.entities)

	@staticmethod
	def addToTest(id):
		EntityManager.entitiesCol.append(id)

	@staticmethod
	def removeToTest(id):
		EntityManager.entitiesCol.remove(id)
