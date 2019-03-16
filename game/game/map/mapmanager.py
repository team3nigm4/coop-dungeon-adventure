# Manages the current map, displays it, and performs various actions on it (collision test)

import math

from game.game.entityclass import entitymanager as em
from game.game.map import maprender as mp
from game.game.map.eventmanager import EventManager as ev
from game.game.map.maptemporarysave import MapTemporarySave as mts
from game.game.map.maploading import MapLoading as ml
from game.screen import gamemanager as gm


class MapManager:
	COEF = 2

	INTERACTION_SOLID = 1
	INTERACTION_EMPTY = 2

	TRANSITION_TIMES = [30, 1, 30]
	TRANSITION_BEGIN = 0
	TRANSITION_LOAD = 1
	TRANSITION_END = 2


	cWidth = None
	cHeight = None
	interaction = []

	zone = "null"
	id = "null"
	entryPos = []
	entry = 0
	defaultEntry = 0

	changeValues = None

	transition = False
	transitionPhase = 0
	transitionCount = 0

	@staticmethod
	def changeRoom():
		zone = MapManager.changeValues[0]
		map = MapManager.changeValues[1]
		entry = MapManager.changeValues[2]

		# If the room if a new map
		if not ml.isMap(zone, map, entry):
			if MapManager.zone == "null":
				MapManager.changeValues[0] = "test"
				MapManager.changeValues[1] = "map1"
				MapManager.changeValues[2] = 0
				MapManager.changeRoom()
				return

		# If a new Zone
		if not zone == MapManager.zone:
			mts.newZone(zone)
		elif MapManager.id == map:
			mts.unload(map)

		# Apply values
		MapManager.zone = zone
		MapManager.id = map
		MapManager.entry = entry

		mts.changeRoom(map, entry)
		# Clear the game before changing
		MapManager.changeValues = None

	@staticmethod
	def checkChangeMap():
		# Default value of change value (without map chnage requested) is none
		if MapManager.changeValues is not None:
			# Prepare the transition
			gm.GameManager.currentScreen.inPause = True
			MapManager.transition = True

	@staticmethod
	def checkCollisionX(entity):
		colBoxSize = entity.halfColSize
		half = colBoxSize[0] * MapManager.COEF
		speed = entity.speed[0] * MapManager.COEF
		position = [entity.pos[0] * MapManager.COEF, entity.pos[1] * MapManager.COEF]

		nextPos = position[0] + speed
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.cWidth:
			posY = [math.floor(position[1] - colBoxSize[1] * MapManager.COEF),
					math.floor(position[1] + colBoxSize[1] * MapManager.COEF)]
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
					entity.setPos([nextPos / MapManager.COEF + 1 / MapManager.COEF + half / MapManager.COEF + 0.001,
								   entity.pos[1]])
					return
		else:
			return

		entity.setPos([position[0] / MapManager.COEF + speed / MapManager.COEF, entity.pos[1]])

	@staticmethod
	def checkCollisionY(entity):
		colBoxSize = entity.halfColSize
		half = colBoxSize[1] * MapManager.COEF
		speed = entity.speed[1] * MapManager.COEF
		position = [entity.pos[0] * MapManager.COEF, entity.pos[1] * MapManager.COEF]

		nextPos = position[1] + speed
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.cHeight:
			posX = [math.floor(position[0] - colBoxSize[0] * MapManager.COEF),
					math.floor(position[0] + colBoxSize[0] * MapManager.COEF)]

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
					entity.setPos([entity.pos[0],
								   nextPos / MapManager.COEF + 1 / MapManager.COEF + half / MapManager.COEF + 0.001])
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
	def display():
		mp.MapRender.display(MapManager.transition)

	@staticmethod
	def init():
		mp.MapRender.init()
		MapManager.changeValues = ["null", "map0", 0]

		MapManager.reserveChange("tuto", "0-2-1", 0)
		MapManager.changeRoom()

	@staticmethod
	def reserveChange(zone, map, entry):
		MapManager.changeValues = [zone, map, entry]

	@staticmethod
	# Change one bloc of the interaction map
	def setTile(position, id):
		MapManager.interaction[MapManager.cHeight - 1 - math.floor(position[1])][math.floor(position[0])] = id

		# Check if entity with collision in the change
		if id == MapManager.INTERACTION_SOLID:
			for i in em.EntityManager.entitiesCol:
				if not em.EntityManager.entities[i].attributes["collision"] == 0:
					e = em.EntityManager.entities[i]
					# Collision Test
					if math.floor(e.pos[0] * MapManager.COEF - e.halfColSize[0] * MapManager.COEF) <= position[0] <= math.floor(
							e.pos[0] * MapManager.COEF + e.halfColSize[0] * MapManager.COEF) and \
							math.floor(e.pos[1] * MapManager.COEF - e.halfColSize[1] * MapManager.COEF) <= position[1] <= math.floor(
						e.pos[1] * MapManager.COEF + e.halfColSize[1] * MapManager.COEF):

						if not e.type == "Player":
							em.EntityManager.remove(e.id)
						else:
							e.applyDamage(1)
							e.setPos(MapManager.entryPos)
							e.setSpeed([0, 0])

	@staticmethod
	def setTileCoef(position, id):
		MapManager.setTile([position[0] * MapManager.COEF, position[1] * MapManager.COEF], id)

	# Change a zone of the interaction map
	@staticmethod
	def setTileSize(position, size, id):
		posX = [math.floor(position[0] * MapManager.COEF - size[0] * MapManager.COEF),
				math.floor(position[0] * MapManager.COEF + size[0] * MapManager.COEF)]
		posY = [math.floor(position[1] * MapManager.COEF - size[1] * MapManager.COEF),
				math.floor(position[1] * MapManager.COEF + size[1] * MapManager.COEF)]

		countX = 0
		countY = 0
		while countX < posX[1] - posX[0] + 1:
			while countY < posY[1] - posY[0] + 1:
				MapManager.setTile([posX[0] + countX, posY[0] + countY], id)
				countY += 1
			countY = 0
			countX += 1


	@staticmethod
	def setupMapValues(interaction, defaultEntry, entryPos):
		MapManager.interaction = interaction
		MapManager.defaultEntry = defaultEntry

		# Set the size of the current map
		cWidth = len(MapManager.interaction[0])
		cHeight = len(MapManager.interaction)
		MapManager.cWidth = cWidth
		MapManager.cHeight = cHeight

		# Create instance of entities and place players
		MapManager.entryPos = entryPos
		em.EntityManager.entities[em.EntityManager.PLAYER_1].setPos(entryPos)
		em.EntityManager.entities[em.EntityManager.PLAYER_2].setPos(entryPos)

	@staticmethod
	def unload():
		mp.MapRender.unload()
		mts.unloadAll()

	@staticmethod
	def update():
		if MapManager.transition:
			if MapManager.transitionPhase > 2:
				# Reset values
				MapManager.transitionCount = 0
				MapManager.transitionPhase = 0
				gm.GameManager.currentScreen.inPause = False
				MapManager.transition = False
			else:
				# If end of each phase
				if MapManager.transitionCount >= MapManager.TRANSITION_TIMES[MapManager.transitionPhase]:
					MapManager.transitionPhase +=1
					MapManager.transitionCount = 0

				else:
					if MapManager.transitionPhase == MapManager.TRANSITION_LOAD:
						MapManager.changeRoom()
					MapManager.transitionCount +=1
		else:
			ev.dispose()
			MapManager.checkChangeMap()
			mp.MapRender.dispose()
