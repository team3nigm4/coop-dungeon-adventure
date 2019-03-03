# Manages the current map, displays it, and performs various actions on it (collision test)

import math

from game.game.entityclass import entitymanager as em
from game.render.shader.shadermanager import ShaderManager as sm
from game.render.shape import shape
from game.render.texture import texture
from game.util import matrix4f
from game.game.map import mapdisplay as mp


class MapManager:
	DATA_MAP_INFO = 0
	DATA_INTERACTIONS = 1
	DATA_ENTRIES = 2
	DATA_ENTITIES = 3

	INTERACTION_SOLID = 1
	INTERACTION_EMPTY = 2

	width = None
	height = None
	interaction = []

	zone = "null"
	id = "null"
	entryPos = []
	entry = 0
	defaultEntry = 0

	changeValues = None

	@staticmethod
	def init():
		mp.MapDisplay.init()

		MapManager.changeRoom("test", "map1", 0)

	@staticmethod
	def display():
		mp.MapDisplay.display()

	@staticmethod
	def checkCollisionX(entity):
		colBoxSize = entity.halfColSize
		half = colBoxSize[0]
		speed = entity.speed[0]
		position = entity.pos

		nextPos = position[0] + speed
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.width:
			posY = [math.floor(position[1] - colBoxSize[1]), math.floor(position[1] + colBoxSize[1])]

			if speed > 0:
				nextPos = math.floor(nextPos + half)
				if MapManager.interaction[MapManager.height - 1 - posY[0]][nextPos] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.height - 1 - posY[1]][
							nextPos] == MapManager.INTERACTION_SOLID:
					entity.setPos([nextPos - half - 0.001, entity.pos[1]])
					return

			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.interaction[MapManager.height - 1 - posY[0]][nextPos] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.height - 1 - posY[1]][
							nextPos] == MapManager.INTERACTION_SOLID:
					entity.setPos([nextPos + 1 + half + 0.001, entity.pos[1]])
					return
		else:
			return

		entity.setPos([position[0] + speed, entity.pos[1]])

	@staticmethod
	def checkCollisionY(entity):
		colBoxSize = entity.halfColSize
		half = colBoxSize[1]
		speed = entity.speed[1]
		position = entity.pos

		nextPos = position[1] + speed
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.height:
			posX = [math.floor(position[0] - colBoxSize[0]), math.floor(position[0] + colBoxSize[0])]

			if speed > 0:
				nextPos = math.floor(nextPos + half)
				if MapManager.interaction[MapManager.height - 1 - nextPos][posX[0]] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.height - 1 - nextPos][
							posX[1]] == MapManager.INTERACTION_SOLID:
					entity.setPos([entity.pos[0], nextPos - half - 0.001])
					return
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.interaction[MapManager.height - 1 - nextPos][posX[0]] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.height - 1 - nextPos][
							posX[1]] == MapManager.INTERACTION_SOLID:
					entity.setPos([entity.pos[0], nextPos + 1 + half + 0.001])
					return
		else:
			return
		entity.setPos([entity.pos[0], position[1] + speed])

	@staticmethod
	def checkEmpty(entity):
		if MapManager.interaction[MapManager.height - 1 - math.floor(entity.pos[1])][
			math.floor(entity.pos[0])] == MapManager.INTERACTION_EMPTY:
			side = [math.floor(entity.pos[0] - entity.halfColSize[0]),
					math.floor(entity.pos[1] + entity.halfColSize[1]),
					math.floor(entity.pos[0] + entity.halfColSize[0]),
					math.floor(entity.pos[1] - entity.halfColSize[1])]

			empty = 0
			if MapManager.interaction[MapManager.height - 1 - side[1]][side[0]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if MapManager.interaction[MapManager.height - 1 - side[1]][side[2]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if MapManager.interaction[MapManager.height - 1 - side[3]][side[2]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if MapManager.interaction[MapManager.height - 1 - side[3]][side[0]] == MapManager.INTERACTION_EMPTY:
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
		mp.MapDisplay.constructMap()

		# Apply values
		MapManager.zone = values[MapManager.DATA_MAP_INFO][0]
		MapManager.id = values[MapManager.DATA_MAP_INFO][1]
		MapManager.defaultEntry = values[MapManager.DATA_MAP_INFO][2]

		MapManager.interaction = values[MapManager.DATA_INTERACTIONS]

		# Setup the event Manager
		from game.game.map.eventmanager import EventManager
		EventManager.setupEvent(values[MapManager.DATA_MAP_INFO][3])

		# Set the size of the current map
		width = len(MapManager.interaction[0])
		height = len(MapManager.interaction)
		MapManager.width = width
		MapManager.height = height

		# Create instance of entities and place players
		MapManager.entry = entry
		MapManager.entryPos = values[MapManager.DATA_ENTRIES]
		em.EntityManager.entities[em.EntityManager.PLAYER_1].setPos(values[MapManager.DATA_ENTRIES])
		em.EntityManager.entities[em.EntityManager.PLAYER_2].setPos(values[MapManager.DATA_ENTRIES])

		for i in range(0, len(values[MapManager.DATA_ENTITIES])):
			args = values[MapManager.DATA_ENTITIES][i][1]
			args.insert(0, (values[MapManager.DATA_ENTITIES][i][0]))
			em.EntityManager.addA(args)

		# Set the camera position

		from game.screen import gamemanager
		cam = gamemanager.GameManager.cam

		cam.setPos([0, 0, cam.pos[2]])
		cam.setMaximum([width, height])

		if width > 18:
			cam.track[0] = True
		else:
			cam.track[0] = False
			cam.addPos([-width / 2, 0, 0])

		if height > 12:
			cam.track[1] = True
		else:
			cam.track[1] = False
			cam.addPos([0, -height / 2, 0])

		cam.goToEntity()
		sm.dispose()

	@staticmethod
	# Change one bloc of the interaction map
	def setTile(position, id):
		MapManager.interaction[MapManager.height - 1 - math.floor(position[1])][math.floor(position[0])] = id

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
		posX = [math.floor(position[0] - size[0]), math.floor(position[0] + size[0])]
		posY = [math.floor(position[1] - size[1]), math.floor(position[1] + size[1])]

		for x in range(posX[0], posX[1] + 1):
			for y in range(posY[0], posY[1] + 1):
				MapManager.setTile([x, y], id)

	@staticmethod
	def reserveChange(values):
		MapManager.changeValues = values

	@staticmethod
	def checkChangeMap():
		if MapManager.changeValues is not None:
			MapManager.changeRoom(MapManager.changeValues[0], MapManager.changeValues[1], MapManager.changeValues[2])

	@staticmethod
	def unload():
		mp.MapDisplay.unload()
