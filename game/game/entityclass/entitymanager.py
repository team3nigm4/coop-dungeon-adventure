# coding=utf-8
# Static class to contain the entity in a map and to manage it
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
		"Decor": 0,
		"Tp": 0,
		"InteractionSwitch": 0,
		"ItemRecoverable": 1,
		"Padlock": 1,
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
	# Entities will collide between them
	entitiesCol = []
	entitiesRemove = []

	# Len of "entities" table
	len = 0

	displayLayer = [[], [], [], []]

	displayBox = True

	# Add an entity if this one have not an id
	@staticmethod
	def addA(args):
		# Insert in args to define the entity the id with checkPlace
		args.insert(entitycollision.EntityCollision.ARGS_ID, EntityManager.checkPlace())
		result = LoadEntity.instance(args)
		if result[0] == "True":
			EntityManager.addWithId(result[1])
		else:
			# No error can append when un-resettable entity in the reset of the map can't be init a time again
			if not result[1] == "No Error":
				Logger.error("LoadEntity", str(result[1]) + "\n" + str(args))

	# Add an entity to a layer of displaying
	@staticmethod
	def addToDisplay(layer, entityId, pos=0):
		# If the entity is not yet in the layer
		if not entityId in EntityManager.displayLayer[layer]:
			if pos < 0 or pos >= len(EntityManager.displayLayer[layer]):
				EntityManager.displayLayer[layer].append(entityId)
			else:
				if pos < len(EntityManager.displayLayer[layer]):
					EntityManager.displayLayer[layer].insert(pos, entityId)
				else:
					EntityManager.displayLayer[layer].append(entityId)

	# Add an entity to interaction tests between entities
	@staticmethod
	def addToTest(entityId):
		# If the entity is not yet in the table of test
		if not entityId in EntityManager.entitiesCol:
			EntityManager.entitiesCol.append(entityId)
		else:
			Logger.error("EnManager", "AddToTest() Error, with " + EntityManager.entities[
				entityId.id].type + " entity adding two same id : " + str(entityId.id))

	# Add an entity if this one have an id
	@staticmethod
	def addWithId(entity):
		id = entity.entityId.id
		if id == EntityManager.len:
			EntityManager.entities.append(entity)
		else:
			EntityManager.entities[id] = entity

		EntityManager.len = len(EntityManager.entities)

	# Find a free id
	@staticmethod
	def checkPlace():
		for i in range(1, EntityManager.len):
			if EntityManager.entities[i].entityId.id == -1:
				return i
		return len(EntityManager.entities)

	# Check all id
	@staticmethod
	def checkId():
		for e in range(2, EntityManager.len - 1):
			if EntityManager.entities[e].getId() != e:
				EntityManager.entities[e].setId(e)

	# Clear all entities except both players
	@staticmethod
	def clear():
		EntityManager.entities = EntityManager.entities[:2]
		EntityManager.entitiesCol = [EntityManager.entities[0].entityId, EntityManager.entities[1].entityId]
		EntityManager.displayLayer = [[], [], [EntityManager.entities[0].entityId, EntityManager.entities[1].entityId],
									  []]

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

	@staticmethod
	def collision(id):
		list = []
		# Set a list arranged by nearest entity
		for i in range(0, len(EntityManager.entitiesCol)):
			if not EntityManager.entitiesCol[i].id == id:
				# Distance between both entity in the test
				dist = mathcda.distOldE(EntityManager.entities[id],
										EntityManager.entities[EntityManager.entitiesCol[i].id])

				# This loop arrange the final list with nearest entity
				j = 0
				while j < len(list):
					if dist < list[j][0]:
						break
					else:
						j += 1
				list.insert(j, [dist, EntityManager.entitiesCol.index(EntityManager.entitiesCol[i])])

		# Test the collision with the other entities
		for a in list:
			EntityManager.testCollision(EntityManager.entities[id],
										EntityManager.entities[EntityManager.entitiesCol[a[1]].id])

	@staticmethod
	def display():
		for i in EntityManager.displayLayer:
			for e in i:
				EntityManager.entities[e.id].display()

		if EntityManager.displayBox:
			for e in EntityManager.entities:
				e.displayBox()

	# Arrange the middle layer with nearest entities to the bottom of the game
	@staticmethod
	def displayMiddleEntity(entityID):
		ent = EntityManager.entities[entityID.id]
		index = EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE].index(entityID)
		# If the entity move up, test its position with entity with lower index
		if ent.pos[1] > ent.oldPos[1]:
			# Check its position with lower entity in the table
			for i in range(index, -1, -1):
				ent2 = EntityManager.entities[EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE][i].id]
				if ent.pos[1] + ent.gapDisplayPos > ent2.pos[1] + ent2.gapDisplayPos:
					EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE].remove(entityID)
					EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE].insert(i, entityID)
		# If the entity move down, test its position with entity with higher index
		elif ent.pos[1] < ent.oldPos[1]:
			# Check its position with higher entity in the table
			for i in range(index, len(EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE]), 1):
				ent2 = EntityManager.entities[EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE][i].id]
				if ent.pos[1] + ent.gapDisplayPos < ent2.pos[1] + ent2.gapDisplayPos:
					EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE].remove(entityID)
					EntityManager.displayLayer[EntityManager.DISPLAY_MIDDLE].insert(i, entityID)

	@staticmethod
	def dispose():
		# Delete entities registered in "entities removed"
		EntityManager.entitiesRemove.reverse()
		for a in EntityManager.entitiesRemove:
			EntityManager.rem(a)
		EntityManager.entitiesRemove = []

	# Re apply somme important effects of un resetable entity after the reset
	@staticmethod
	def entityEffectAfterReset():
		for e in EntityManager.entities:
			if not EntityManager.isResetable(e):
				if hasattr(e, "checkState"):
					e.checkState()

	@staticmethod
	def init():
		from game.main.config import Config

		EntityManager.displayBox = Config.values["general"]["debug"]

		EntityManager.len = 0

		EntityManager.entities = []
		EntityManager.entitiesCol = []
		EntityManager.entitiesRemove = []
		EntityManager.displayLayer = [[], [], [], []]

	@staticmethod
	def isResetable(e):
		type = e.type
		count = 0
		# Spawn can be reset, but spawn can contain an un resetable entity.
		# Loop to test is the spawn contains this type ogf entity.
		if type == "Spawn":
			while type == "Spawn":
				temp = e.entityInfo
				for i in range(count):
					temp = temp[3]

				if not temp[0] == "Spawn":
					type = temp[0]
				else:
					count += 1

		return EntityManager.LIST_RESET[type] == EntityManager.TO_RESET

	# Remove an entity
	@staticmethod
	def rem(info):
		id = info[0].id

		# Unload the entity
		EntityManager.entities[id].unload()

		del EntityManager.entities[id]

		EntityManager.len = len(EntityManager.entities)
		# Print the removing ?
		if info[1]:
			Logger.info("EnManager", "Remove entity n°" + str(id))

		if id != len(EntityManager.entities):
			for i in range(id, EntityManager.len):
				EntityManager.entities[i].entityId.id -=1

	# Entity can't be remove during a loop, so they are registered
	@staticmethod
	def remove(entityId, printRemove):
		for e in EntityManager.entitiesRemove:
			if e[0] == entityId:
				return
		EntityManager.entitiesRemove.append([entityId, printRemove])

	# Delete an entity to a layer of displaying
	@staticmethod
	def removeToDipslay(layer, entityId):
		if entityId in EntityManager.displayLayer[layer]:
			EntityManager.displayLayer[layer].remove(entityId)

	# Delete an entity to the global entity test
	@staticmethod
	def removeToTest(entityId):
		if entityId in EntityManager.entitiesCol:
			EntityManager.entitiesCol.remove(entityId)
		else:
			Logger.error("EnManager", "RemoveToTest() Error " + EntityManager.entities[
				entityId.id].type + " entity want to be remove from entityCol, id : " + str(entityId.id))

	# Print the current status of entitymanager
	@staticmethod
	def status():
		Logger.info("EnManager", "\n status with len(" + str(EntityManager.len) + ") :\n")
		for e in EntityManager.entities:
			Logger.info("EnManager", "Entity" + str(e.entityId.id) + ", entityType" + e.type)

	@staticmethod
	def setEntities(entities):
		EntityManager.entities = entities
		EntityManager.len = len(EntityManager.entities)

	# MapTemporarySave set the value of this class after a map changing
	@staticmethod
	def setValues(entities, entitiesCol, displayLayer):
		EntityManager.setEntities(entities)
		EntityManager.entitiesCol = entitiesCol
		EntityManager.displayLayer = displayLayer

	# Collision with aabb rect method
	@staticmethod
	def testCollision(ent1, ent2):
		if not (ent2.pos[0] - ent2.halfColSize[0] >= ent1.pos[0] + ent1.halfColSize[0] or
				ent2.pos[0] + ent2.halfColSize[0] <= ent1.pos[0] - ent1.halfColSize[0] or
				ent2.pos[1] - ent2.halfColSize[1] >= ent1.halfColSize[1] + ent1.pos[1] or
				ent2.pos[1] + ent2.halfColSize[1] <= ent1.pos[1] - ent1.halfColSize[1]):
			ent2.collision(ent1)

	# Unload the entity, if reset don't unload un-resetable entity
	@staticmethod
	def discharge(reset=False):
		id = 2
		if EntityManager.len > 1:
			for i in range(2, EntityManager.len):
				if reset and not EntityManager.isResetable(EntityManager.entities[id]):
					id += 1
				else:
					EntityManager.entities[id].unload()
					del EntityManager.entities[id]
		EntityManager.len = len(EntityManager.entities)

	# Final unload of the class
	@staticmethod
	def unload():
		del EntityManager.displayLayer
		del EntityManager.entities
		del EntityManager.entitiesCol
		del EntityManager.entitiesRemove
