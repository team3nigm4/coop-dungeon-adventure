# Manage every entity of the game


import math

from game.game.entityclass import entitycollision
from game.util import math as mathcda

class EntityManager:
	PLAYER_1 = 0
	PLAYER_2 = 1

	entities = []
	entitiesCol = []
	entitiesRemove = []

	len = 0

	@staticmethod
	def init():
		EntityManager.len = 0

	@staticmethod
	def update():
		e = EntityManager.len - 1
		while e >= 0:
			EntityManager.entities[e].update()
			if EntityManager.entities[e].testCol:
				EntityManager.collision(e)
			e -= 1

	@staticmethod
	def display():
		e = EntityManager.len - 1
		while e >= 0:
			EntityManager.entities[e].display()
			e -= 1

	@staticmethod
	def collision(entityId):
		list = []
		for i in range(0, len(EntityManager.entitiesCol)):
			if not EntityManager.entitiesCol[i] == entityId:
				dist = mathcda.distOldE(EntityManager.entities[entityId], EntityManager.entities[EntityManager.entitiesCol[i]])

				j = 0
				while j < len(list):
					if dist < list[j][0]:
						break
					else:
						j += 1
				list.insert(j, [dist, EntityManager.entitiesCol.index(EntityManager.entitiesCol[i])])

		for a in list:
			EntityManager.testCollision(EntityManager.entities[entityId],
										EntityManager.entities[EntityManager.entitiesCol[a[1]]])

	@staticmethod
	# Collision rect aabb
	def testCollision(ent1, ent2):
		if not (ent2.pos[0] - ent2.halfColSize[0] >= ent1.pos[0] + ent1.halfColSize[0] or
				ent2.pos[0] + ent2.halfColSize[0] <= ent1.pos[0] - ent1.halfColSize[0] or
				ent2.pos[1] - ent2.halfColSize[1] >= ent1.halfColSize[1] + ent1.pos[1] or
				ent2.pos[1] + ent2.halfColSize[1] <= ent1.pos[1] - ent1.halfColSize[1]):
			ent2.collision(ent1)

	@staticmethod
	def add(entity):
		id = EntityManager.checkPlace()
		entity.setId(id)
		if entity.id == EntityManager.len:
			EntityManager.entities.append(entity)
		else:
			EntityManager.entities[entity.id] = entity

		if isinstance(entity, entitycollision.EntityCollision):
			if entity.testCol:
				EntityManager.addToTest(entity.id)

		EntityManager.len = len(EntityManager.entities)

	@staticmethod
	def rem(entity):
		id = entity[0]

		# Unload the entity
		EntityManager.entities[id].unload()

		if isinstance(EntityManager.entities[id], entitycollision.EntityCollision):
			if EntityManager.entities[id].testCol:
				EntityManager.entitiesCol.remove(id)

		if id == len(EntityManager.entities) - 1:
			del EntityManager.entities[id]
		else:
			EntityManager.entities[id] = entitycollision.EntityCollision(["NULL", [0, 0]])
			EntityManager.entities[id].setId(-1)

		EntityManager.len = len(EntityManager.entities)
		if entity[1]:
			print("Remove the entity,", id)

	@staticmethod
	def remove(id, display=True):
		EntityManager.entitiesRemove.append([id, display])

	@staticmethod
	def dispose():
		EntityManager.entitiesRemove.sort(reverse=True)
		for a in EntityManager.entitiesRemove:
			EntityManager.rem(a)
		EntityManager.entitiesRemove = []

	@staticmethod
	def clear():
		# Delete h
		if EntityManager.len > 1:
			for i in range(2, EntityManager.len):
				EntityManager.entities[2].unload()
				EntityManager.entities.remove(EntityManager.entities[2])

		EntityManager.entitiesCol = [EntityManager.PLAYER_1, EntityManager.PLAYER_2]
		EntityManager.len = len(EntityManager.entities)

	@staticmethod
	def checkPlace():
		for i in range(0, EntityManager.len):
			if EntityManager.entities[i].id == -1:
				return i
		return len(EntityManager.entities)

	@staticmethod
	def addToTest(id):
		if not id in EntityManager.entitiesCol:
			EntityManager.entitiesCol.append(id)
		else:
			print("(EntityManager - addToTest() ) Error two entities with same id want to be place on entityCol, id :",
				  id)

	@staticmethod
	def removeToTest(id):
		if id in EntityManager.entitiesCol:
			EntityManager.entitiesCol.remove(id)
		else:
			print("(EntityManager - removeToTest()) Error none entity want to be remove from entityCol, id : ", id)

	@staticmethod
	def status():
		print("\nEntityManager status:\n")
		for i in range(0, EntityManager.len):
			print("Entity", EntityManager.entities[i].id, ", entityType", EntityManager.entities[i].type)

	@staticmethod
	def unload():
		print("\nUnload EntityManager :")
		for e in EntityManager.entities:
			e.unload()
		print("\n")
