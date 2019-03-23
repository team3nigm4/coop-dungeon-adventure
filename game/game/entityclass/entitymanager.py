# Manage every entity of the game

from game.game.entityclass.loadentity import LoadEntity
from game.game.entityclass import entitycollision
from game.util import math as mathcda
from game.util.logger import Logger


class EntityManager:
	PLAYER_1 = 0
	PLAYER_2 = 1

	ENTITY_NO_ERROR = ["SpawnPoint"]

	DISPLAY_DOWN = 0
	DISPLAY_DOWN2 = 1
	DISPLAY_MIDDLE = 2
	DISPLAY_UP = 3

	# reset = 0, no reset = 1
	LIST_RESET = {
		"Null": 0,
		"ActivationBlock": 0,
		"ActivationPlate": 0,
		"Arrow": 0,
		"Bat": 0,
		"Bridge": 0,
		"Door": 0,
		"ItemRecoverable": 1,
		"LockedDoor": 1,
		"Mannequin": 0,
		"Player": 1,
		"PressurePlate": 0,
		"SlidingBlock": 0,
		"Spawn": 0,
		"Spider": 0,
		"TogglePlate": 0
	}

	TO_RESET = 0
	NO_RESET = 1

	entities = []
	entitiesCol = []
	entitiesRemove = []

	len = 0

	displayLayer = [[], [], [], []]

	displayBox = True

	@staticmethod
	def addA(args):
		args.insert(entitycollision.EntityCollision.ARGS_ID, EntityManager.checkPlace())
		entity = LoadEntity.instance(args)
		if entity != False:
			EntityManager.addWithId(entity)
		else:
			if not args[0] in EntityManager.ENTITY_NO_ERROR:
				print("Error: wrong arguments to instance an entity:\n", args)

	@staticmethod
	def addToDisplay(layer, id, pos=0):
		if not id in EntityManager.displayLayer[layer]:
			if pos < 0 or pos >= len(EntityManager.displayLayer[layer]):
				EntityManager.displayLayer[layer].append(id)
			else:
				if pos < len(EntityManager.displayLayer[layer]):
					EntityManager.displayLayer[layer].insert(pos, id)
				else:
					EntityManager.displayLayer[layer].append(id)

	@staticmethod
	def addToTest(id):
		if not id in EntityManager.entitiesCol:
			EntityManager.entitiesCol.append(id)
		else:
			print("(EntityManager - addToTest()) Error, adding two same id :", id, ", type:",
				  EntityManager.entities[id].type)

	@staticmethod
	def addWithId(entity):
		if entity.id == EntityManager.len:
			EntityManager.entities.append(entity)
		else:
			EntityManager.entities[entity.id] = entity

		EntityManager.len = len(EntityManager.entities)

	@staticmethod
	def checkPlace():
		for i in range(1, EntityManager.len):
			if EntityManager.entities[i].id == -1:
				return i
		return len(EntityManager.entities)

	@staticmethod
	def checkId():
		for e in range(3, EntityManager.len):
			idM =  EntityManager.entities[e-1].id
			print(EntityManager.entities[e])
			if EntityManager.entities[e].id - idM > 1:
				EntityManager.entities[e].unloadToEntityManager()
				EntityManager.entities[e].id = idM + 1
				EntityManager.entities[e].chargeToEntityManager()

	@staticmethod
	def clear():
		EntityManager.entities = EntityManager.entities[:2]
		EntityManager.entitiesCol = [EntityManager.PLAYER_1, EntityManager.PLAYER_2]
		EntityManager.displayLayer = [[], [], [EntityManager.PLAYER_1, EntityManager.PLAYER_2], []]

		EntityManager.len = len(EntityManager.entities)

	@staticmethod
	def collision(entityId):
		list = []
		for i in range(0, len(EntityManager.entitiesCol)):
			if not EntityManager.entitiesCol[i] == entityId:
				dist = mathcda.distOldE(EntityManager.entities[entityId],
										EntityManager.entities[EntityManager.entitiesCol[i]])

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
	def display():
		for i in EntityManager.displayLayer:
			for e in i:
				EntityManager.entities[e].display()

		if EntityManager.displayBox:
			for e in EntityManager.entities:
				e.displayBox()

	@staticmethod
	def displayMiddleEntity(entityID):
		ent = EntityManager.entities[entityID]
		index = EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE].index(entityID)
		if ent.pos[1] > ent.oldPos[1]:
			for i in range(index, -1, -1):
				ent2 = EntityManager.entities[EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE][i]]
				if ent.pos[1] + ent.gapDisplayPos > ent2.pos[1] + ent2.gapDisplayPos:
					EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE].remove(entityID)
					EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE].insert(i, entityID)
		elif ent.pos[1] < ent.oldPos[1]:
			for i in range(index, len(EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE]), 1):
				ent2 = EntityManager.entities[EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE][i]]
				if ent.pos[1] + ent.gapDisplayPos < ent2.pos[1] + ent2.gapDisplayPos:
					EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE].remove(entityID)
					EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE].insert(i, entityID)

	@staticmethod
	def dispose():
		EntityManager.entitiesRemove.sort(reverse=True)
		for a in EntityManager.entitiesRemove:
			EntityManager.rem(a)
		EntityManager.entitiesRemove = []

	@staticmethod
	def entityEffectAfterReset():
		for e in EntityManager.entities:
			if not EntityManager.isResetable(e):
				if hasattr(e, "checkState"):
					e.checkState()

	@staticmethod
	def init():
		EntityManager.len = 0

	@staticmethod
	def isResetable(e):
		type = e.type
		count = 0
		if type == "Spawn":
			while type == "Spawn":
				temp = e.entityInfo
				for i in range(count):
					temp = temp[3]

				if not temp[0] == "Spawn":
					type = temp[0]
				else:
					count +=1

		return EntityManager.LIST_RESET[type] == EntityManager.TO_RESET

	@staticmethod
	def rem(entity):
		id = entity[0]

		# Unload the entity
		EntityManager.entities[id].unload()

		if id == len(EntityManager.entities) - 1:
			del EntityManager.entities[id]
		else:
			EntityManager.entities[id] = entitycollision.EntityCollision(["Null", -1, [0, 0]])

		EntityManager.len = len(EntityManager.entities)
		if entity[1]:
			Logger.info("ENTITY MANAGER", "Remove entity n°" + str(id))

	@staticmethod
	def remove(id, display=True):
		EntityManager.entitiesRemove.append([id, display])

	@staticmethod
	def removeToDipslay(layer, id):
		if id in EntityManager.displayLayer[layer]:
			EntityManager.displayLayer[layer].remove(id)

	@staticmethod
	def removeToTest(id):
		if id in EntityManager.entitiesCol:
			EntityManager.entitiesCol.remove(id)
		else:
			print("(EntityManager - removeToTest()) Error none entity want to be remove from entityCol, id : ", id)

	@staticmethod
	def status():
		print("\nEntityManager status len(", EntityManager.len, ") :\n")
		for e in EntityManager.entities:
			print("Entity", e.id, ", entityType", e.type)

	@staticmethod
	def setEntities(entities):
		EntityManager.entities = entities
		EntityManager.len = len(EntityManager.entities)

	@staticmethod
	def setValues(entities, entitiesCol, displayLayer):
		EntityManager.setEntities(entities)
		EntityManager.entitiesCol = entitiesCol
		EntityManager.displayLayer = displayLayer

	@staticmethod
	# Collision rect aabb
	def testCollision(ent1, ent2):
		if not (ent2.pos[0] - ent2.halfColSize[0] >= ent1.pos[0] + ent1.halfColSize[0] or
				ent2.pos[0] + ent2.halfColSize[0] <= ent1.pos[0] - ent1.halfColSize[0] or
				ent2.pos[1] - ent2.halfColSize[1] >= ent1.halfColSize[1] + ent1.pos[1] or
				ent2.pos[1] + ent2.halfColSize[1] <= ent1.pos[1] - ent1.halfColSize[1]):
			ent2.collision(ent1)

	@staticmethod
	def unload(reset=False):
		id = 2
		if EntityManager.len > 1:
			for i in range(2, EntityManager.len):
				if (reset and not EntityManager.isResetable(EntityManager.entities[id])):
					id += 1
				else:
					EntityManager.entities[id].unload()
					del EntityManager.entities[id]
		EntityManager.len = len(EntityManager.entities)

	@staticmethod
	def update():
		e = EntityManager.len - 1
		while e >= 0:
			EntityManager.entities[e].update()
			if EntityManager.entities[e].testCol:
				EntityManager.collision(e)
			e -= 1

		for e in EntityManager.entities:
			e.dispose()
