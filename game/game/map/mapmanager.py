# Manages the current map, displays it, and performs various actions on it (collision test)

import math

from game.game.entityclass import entitymanager as em
from game.render.shader.shadermanager import ShaderManager as sm
from game.game.map import maprender as mp


class MapManager:
	DATA_MAP_INFO = 0
	DATA_INTERACTIONS = 1
	DATA_ENTRIES = 2
	DATA_ENTITIES = 3

	COEF = 2

	INTERACTION_SOLID = 1
	INTERACTION_EMPTY = 2

	cWidth = None
	cHeight = None
	interaction = []

	zone = "null"
	id = "null"
	entryPos = []
	entry = 0
	defaultEntry = 0

	changeValues = None

	@staticmethod
	def init():
		mp.MapRender.init()

		MapManager.changeRoom("test", "map4", 0)

	@staticmethod
	def display():
		mp.MapRender.display()

	@staticmethod
	def checkCollisionX(entity):
		colBoxSize = entity.halfColSize
		half = colBoxSize[0] * MapManager.COEF
		speed = entity.speed[0] * MapManager.COEF
		position = [entity.pos[0] * MapManager.COEF, entity.pos[1] * MapManager.COEF]

		nextPos = position[0] + speed
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.cWidth:
			posY = [math.floor(position[1] - colBoxSize[1]  * MapManager.COEF), math.floor(position[1] + colBoxSize[1]  * MapManager.COEF)]
			if speed > 0:
				nextPos = math.floor(nextPos + half)
				if MapManager.interaction[MapManager.cHeight - 1 - posY[0]][nextPos] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.cHeight - 1 - posY[1]][
							nextPos] == MapManager.INTERACTION_SOLID:
					entity.setPos([nextPos / MapManager.COEF - half / MapManager.COEF - 0.001, entity.pos[1]])
					return
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.interaction[MapManager.cHeight - 1 - posY[0]][nextPos] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.cHeight - 1 - posY[1]][
							nextPos] == MapManager.INTERACTION_SOLID:
					entity.setPos([nextPos / MapManager.COEF + 1 / MapManager.COEF + half / MapManager.COEF + 0.001, entity.pos[1]])
					return
		else:
			return

		entity.setPos([position[0] / MapManager.COEF + speed / MapManager.COEF, entity.pos[1]])

	@staticmethod
	def checkCollisionY(entity):
		colBoxSize = entity.halfColSize
		half = colBoxSize[1]  * MapManager.COEF
		speed = entity.speed[1]  * MapManager.COEF
		position = [entity.pos[0] * MapManager.COEF, entity.pos[1] * MapManager.COEF]

		nextPos = position[1] + speed
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.cHeight:
			posX = [math.floor(position[0] - colBoxSize[0] * MapManager.COEF), math.floor(position[0] + colBoxSize[0] * MapManager.COEF)]

			if speed > 0:
				nextPos = math.floor(nextPos + half)
				if MapManager.interaction[MapManager.cHeight - 1 - nextPos][posX[0]] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.cHeight - 1 - nextPos][
							posX[1]] == MapManager.INTERACTION_SOLID:
					entity.setPos([entity.pos[0], nextPos / MapManager.COEF - half / MapManager.COEF - 0.001])
					return
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.interaction[MapManager.cHeight - 1 - nextPos][posX[0]] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.cHeight - 1 - nextPos][
							posX[1]] == MapManager.INTERACTION_SOLID:
					entity.setPos([entity.pos[0], nextPos / MapManager.COEF + 1 / MapManager.COEF + half / MapManager.COEF + 0.001])
					return
		else:
			return
		entity.setPos([entity.pos[0], position[1] / MapManager.COEF + speed / MapManager.COEF])

	@staticmethod
	def checkEmpty(entity):
		if MapManager.interaction[MapManager.cHeight - 1 - math.floor(entity.pos[1] * MapManager.COEF)][
			math.floor(entity.pos[0] * MapManager.COEF)] == MapManager.INTERACTION_EMPTY:
			side = [math.floor(entity.pos[0] * MapManager.COEF - entity.halfColSize[0] * MapManager.COEF),
					math.floor(entity.pos[1] * MapManager.COEF + entity.halfColSize[1] * MapManager.COEF),
					math.floor(entity.pos[0] * MapManager.COEF + entity.halfColSize[0] * MapManager.COEF),
					math.floor(entity.pos[1] * MapManager.COEF - entity.halfColSize[1] * MapManager.COEF)]

			empty = 0
			if MapManager.interaction[MapManager.cHeight - 1 - side[1]][side[0]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if MapManager.interaction[MapManager.cHeight - 1 - side[1]][side[2]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if MapManager.interaction[MapManager.cHeight - 1 - side[3]][side[2]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if MapManager.interaction[MapManager.cHeight - 1 - side[3]][side[0]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if empty > 1:
				if not entity.type == "Player":
					em.EntityManager.remove(entity.id)
				else:
					entity.applyDamage(1)
					entity.setPos(MapManager.entryPos)
					entity.setSpeed([0, 0])

	@staticmethod
	def changeRoom(zone, map, entry):
		# Clear the game before changing
		em.EntityManager.clear()
		MapManager.changeValues = None

		# Load new room
		from game.game.map import maploading
		values = maploading.loadMap(zone, map, entry)

		# Apply values
		MapManager.zone = values[MapManager.DATA_MAP_INFO][0]
		MapManager.id = values[MapManager.DATA_MAP_INFO][1]
		MapManager.defaultEntry = values[MapManager.DATA_MAP_INFO][2]

		MapManager.interaction = values[MapManager.DATA_INTERACTIONS]

		# Setup the event Manager
		from game.game.map.eventmanager import EventManager
		EventManager.setupEvent(values[MapManager.DATA_MAP_INFO][3])

		# Set the size of the current map
		cWidth = len(MapManager.interaction[0])
		cHeight = len(MapManager.interaction)
		MapManager.cWidth = cWidth
		MapManager.cHeight = cHeight

		# Create instance of entities and place players
		MapManager.entry = entry
		MapManager.entryPos = values[MapManager.DATA_ENTRIES]
		em.EntityManager.entities[em.EntityManager.PLAYER_1].setPos(values[MapManager.DATA_ENTRIES])
		em.EntityManager.entities[em.EntityManager.PLAYER_2].setPos(values[MapManager.DATA_ENTRIES])

		for i in range(0, len(values[MapManager.DATA_ENTITIES])):
			args = values[MapManager.DATA_ENTITIES][i][1]
			args.insert(0, (values[MapManager.DATA_ENTITIES][i][0]))
			em.EntityManager.addA(args)

		mp.MapRender.constructMap()

	@staticmethod
	def setTileCoef(position, id):
		MapManager.setTile([position[0] * MapManager.COEF, position[1] * MapManager.COEF], id)

	@staticmethod
	# Change one bloc of the interaction map
	def setTile(position, id):
		print("add a tile", math.floor(position[0]), math.floor(position[1]))
		MapManager.interaction[MapManager.cHeight - 1 - math.floor(position[1])][math.floor(position[0])] = id

		# Check if entity with collision in the change
		if id == MapManager.INTERACTION_SOLID:
			for i in em.EntityManager.entitiesCol:
				if not em.EntityManager.entities[i].attributes["collision"] == 0:
					e = em.EntityManager.entities[i]
					# Collision Test
					if math.floor(e.pos[0] - e.halfColSize[0]) <= position[0] <= math.floor(
							e.pos[0] + e.halfColSize[0]) and \
							math.floor(e.pos[1] - e.halfColSize[1]) <= position[1] <= math.floor(
						e.pos[1] + e.halfColSize[1]):

						if not e.type == "Player":
							em.EntityManager.remove(e.id)
						else:
							e.applyDamage(1)
							e.setPos(MapManager.entryPos)
							e.setSpeed([0, 0])

	# Change a zone of the interaction map
	@staticmethod
	def setTileSize(position, size, id):
		posX = [math.floor(position[0] * MapManager.COEF - size[0] * MapManager.COEF), math.floor(position[0] * MapManager.COEF + size[0] * MapManager.COEF)]
		posY = [math.floor(position[1] * MapManager.COEF - size[1] * MapManager.COEF), math.floor(position[1] * MapManager.COEF + size[1] * MapManager.COEF)]

		countX = 0
		countY = 0
		print("infemX", posX[1] - posX[0] + 1, posX)
		print("infemY", posY[1] - posY[0] + 1, posY)
		while countX < posX[1] - posX[0] + 1:
			while countY < posY[1] - posY[0] + 1:
				MapManager.setTile([posX[0] + countX, posY[0] + countY], id)
				countY += 1
			countY = 0
			countX += 1

	@staticmethod
	def reserveChange(values):
		MapManager.changeValues = values

	@staticmethod
	def dispose():
		MapManager.checkChangeMap()
		mp.MapRender.dispose()

	@staticmethod
	def checkChangeMap():
		if MapManager.changeValues is not None:
			MapManager.changeRoom(MapManager.changeValues[0], MapManager.changeValues[1], MapManager.changeValues[2])

	@staticmethod
	def unload():
		mp.MapRender.unload()
