# Manage every entity of the game

import  math

class EntityManager:
	PLAYER_1 = 0
	PLAYER_2 = 1

	entities = []
	entitiesCol = []
	wantRemove = []

	len = 0

	@staticmethod
	def init():
		EntityManager.len = 0

	@staticmethod
	def update():
		e = EntityManager.len - 1
		while e >= 0:
			EntityManager.entities[e].update()
			e -= 1

	@staticmethod
	def display():
		e = EntityManager.len - 1
		while e >= 0:
			EntityManager.entities[e].display()
			e -= 1

	@staticmethod
	def collision():	
		for i in range(0, len(EntityManager.entitiesCol) - 1):
			nbEntity = len(EntityManager.entitiesCol) - (1 + i)
			list = []
			for a in range(1 + i, len(EntityManager.entitiesCol)):
				dist = math.sqrt((EntityManager.entities[EntityManager.entitiesCol[i]].oldPos[0] -
								  EntityManager.entities[EntityManager.entitiesCol[a]].oldPos[0]) ** 2 +
								 (EntityManager.entities[EntityManager.entitiesCol[i]].oldPos[1] -
								  EntityManager.entities[EntityManager.entitiesCol[a]].oldPos[1]) ** 2)

				j = 0
				while j < len(list):
					if dist < list[j][0]:
						break
					else:
						j +=1
				list.insert(j, [dist , EntityManager.entitiesCol[a], j, len(list)])

			for a in list:
				EntityManager.testCollision(EntityManager.entities[EntityManager.entitiesCol[i]],
											EntityManager.entities[EntityManager.entitiesCol[a[1]]])

	@staticmethod
	# Collision rect aabb
	def testCollision(ent1, ent2):
		if not(ent2.pos[0] - ent2.halfColSize[0] >= ent1.pos[0] + ent1.halfColSize[0] or
			ent2.pos[0] + ent2.halfColSize[0] <= ent1.pos[0] - ent1.halfColSize[0] or
			ent2.pos[1] - ent2.halfColSize[1] >= ent1.halfColSize[1] + ent1.pos[1] or
			ent2.pos[1] + ent2.halfColSize[1] <= ent1.pos[1] - ent1.halfColSize[1]):
			ent2.collision(ent1)
			ent1.collision(ent2)

	@staticmethod
	def add(entity):

		if entity.id == EntityManager.len:
			EntityManager.entities.append(entity)
		else:
			EntityManager.entities[entity.id] = entity

		EntityManager.len = len(EntityManager.entities)

	@staticmethod
	def rem(id):
		# Unload the entity
		EntityManager.entities[id].unload()
		if EntityManager.entities[id].entCol:
			EntityManager.entitiesCol.remove(id)

		if id == len(EntityManager.entities) - 1:
			del EntityManager.entities[id]
			EntityManager.entities.remove(id)
		else:
			from game.game.entityclass import entity
			EntityManager.entities[id] = entity.Entity([0, [0, 0]])
			EntityManager.entities[id].setId(-1)

		EntityManager.len = len(EntityManager.entities)
		print("remove", len(EntityManager.entities), " and ", len(EntityManager.entitiesCol))

	@staticmethod
	def remove(id):
		EntityManager.wantRemove.append(id)

	@staticmethod
	def dispose():
		for a in EntityManager.wantRemove:
			EntityManager.rem(a)
		EntityManager.wantRemove = []


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


	@staticmethod
	def unload():
		print("\nUnload EntityManager :")
		for e in EntityManager.entities:
			e.unload()
		print("\n")
