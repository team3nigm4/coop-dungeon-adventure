# Static class to manage the current map, displays it, and performs various actions on it (collision test)

import math

from game.game.entityclass import entitymanager as em
from game.game.map import maprender as mp
from game.game.map.eventmanager import EventManager as ev
from game.game.map import maptemporarysave as mts
from game.game.map.maploading import MapLoading as ml
from game.screen import gamemanager as gm
from game.util import math as mathcda


class MapManager:
	COEF = 2

	INTERACTION_SOLID = 1
	INTERACTION_EMPTY = 2

	TRANSITION_TIMES = [20, 10, 20]
	TRANSITION_BEGIN = 0
	TRANSITION_LOAD = 1
	TRANSITION_END = 2

	interaction = [[]]
	iWidth = 0
	iHeight = 0

	collideTest = True

	zone = "null"
	id = "null"
	entryInfo = []
	entry = -1
	defaultEntry = 0

	changeValues = []
	exitPos = 4

	transition = False
	transitionPhase = 0
	transitionCount = 0

	# Change the current map
	@staticmethod
	def changeRoom():
		zone = MapManager.changeValues[0]
		map = MapManager.changeValues[1]
		entry = MapManager.changeValues[2]

		# If map exists
		if not ml.isMap(zone, map, entry):
			if MapManager.zone == "null":
				MapManager.changeValues[0] = "intro"
				MapManager.changeValues[1] = "hall"
				MapManager.changeValues[2] = 0
				MapManager.changeRoom()
				return

		# If the map is in a new zone
		if not zone == MapManager.zone:
			mts.MapTemporarySave.newZone(zone)

		# Apply values
		zoneTemp = MapManager.zone
		MapManager.collideTest = False
		MapManager.zone = zone
		MapManager.id = map
		MapManager.entry = entry

		# Map reset
		if MapManager.exitPos == 4 and not zoneTemp == "null":
			mts.MapTemporarySave.changeRoom(map, entry, True)
		# Map change
		else:
			mts.MapTemporarySave.changeRoom(map, entry)

		# Clear the game before changing
		MapManager.changeValues = []
		MapManager.collideTest = True

	# Check at each frame if a map change is requested
	@staticmethod
	def checkChangeMap():
		# Default value of change value (without map change requested) is []
		if MapManager.changeValues:
			# Prepare the transition
			gm.GameManager.currentScreen.mapChange = True
			MapManager.transition = True
			mp.MapRender.setTransitionPos([999999, 999999])

	@staticmethod
	def checkCollisionX(entity):
		colBoxSize = entity.halfColSize
		half = colBoxSize[0] * MapManager.COEF
		speed = entity.speed[0] * MapManager.COEF
		position = [entity.pos[0] * MapManager.COEF, entity.pos[1] * MapManager.COEF]

		# Next position of the player in x
		nextPos = position[0] + speed
		# If movement in the range of the map
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.iWidth:
			posY = [math.floor(position[1] - colBoxSize[1] * MapManager.COEF),
					math.floor(position[1] + colBoxSize[1] * MapManager.COEF)]
			if speed > 0:
				nextPos = math.floor(nextPos + half)
				if MapManager.interaction[MapManager.iHeight - 1 - posY[0]][nextPos] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.iHeight - 1 - posY[1]][
							nextPos] == MapManager.INTERACTION_SOLID:
					entity.setPos([nextPos / MapManager.COEF - half / MapManager.COEF - 0.001, entity.pos[1]])
					return
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.interaction[MapManager.iHeight - 1 - posY[0]][nextPos] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.iHeight - 1 - posY[1]][
							nextPos] == MapManager.INTERACTION_SOLID:
					entity.setPos([nextPos / MapManager.COEF + 1 / MapManager.COEF + half / MapManager.COEF + 0.001,
								   entity.pos[1]])
					return
		else:
			return

		# Set the real position without collision
		entity.setPos([position[0] / MapManager.COEF + speed / MapManager.COEF, entity.pos[1]])

	@staticmethod
	def checkCollisionY(entity):
		colBoxSize = entity.halfColSize
		half = colBoxSize[1] * MapManager.COEF
		speed = entity.speed[1] * MapManager.COEF
		position = [entity.pos[0] * MapManager.COEF, entity.pos[1] * MapManager.COEF]

		# Next position of the player in y
		nextPos = position[1] + speed
		# If movement in the range of the map
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.iHeight:
			posX = [math.floor(position[0] - colBoxSize[0] * MapManager.COEF),
					math.floor(position[0] + colBoxSize[0] * MapManager.COEF)]

			if speed > 0:
				nextPos = math.floor(nextPos + half)
				if MapManager.interaction[MapManager.iHeight - 1 - nextPos][posX[0]] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.iHeight - 1 - nextPos][
							posX[1]] == MapManager.INTERACTION_SOLID:
					entity.setPos([entity.pos[0], nextPos / MapManager.COEF - half / MapManager.COEF - 0.001])
					return
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.interaction[MapManager.iHeight - 1 - nextPos][posX[0]] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.iHeight - 1 - nextPos][
							posX[1]] == MapManager.INTERACTION_SOLID:
					entity.setPos([entity.pos[0],
								   nextPos / MapManager.COEF + 1 / MapManager.COEF + half / MapManager.COEF + 0.001])
					return
		else:
			return

		# Set the real position without collision
		entity.setPos([entity.pos[0], position[1] / MapManager.COEF + speed / MapManager.COEF])

	@staticmethod
	def checkEmpty(entity):
		if MapManager.interaction[MapManager.iHeight - 1 - math.floor(entity.pos[1] * MapManager.COEF)][
			math.floor(entity.pos[0] * MapManager.COEF)] == MapManager.INTERACTION_EMPTY:
			side = [math.floor(entity.pos[0] * MapManager.COEF - entity.halfColSize[0] * MapManager.COEF),
					math.floor(entity.pos[1] * MapManager.COEF + entity.halfColSize[1] * MapManager.COEF),
					math.floor(entity.pos[0] * MapManager.COEF + entity.halfColSize[0] * MapManager.COEF),
					math.floor(entity.pos[1] * MapManager.COEF - entity.halfColSize[1] * MapManager.COEF)]

			empty = 0
			if MapManager.interaction[MapManager.iHeight - 1 - side[1]][side[0]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if MapManager.interaction[MapManager.iHeight - 1 - side[1]][side[2]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if MapManager.interaction[MapManager.iHeight - 1 - side[3]][side[2]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if MapManager.interaction[MapManager.iHeight - 1 - side[3]][side[0]] == MapManager.INTERACTION_EMPTY:
				empty += 1

			if empty > 1:
				if not entity.type == "Player":
					em.EntityManager.remove(entity.entityId, entity.type)
				else:
					entity.applyDamage(1)
					entity.setPos(MapManager.entryInfo[0])
					entity.setSpeed([0, 0])

	@staticmethod
	def display():
		mp.MapRender.display(MapManager.transition)

	@staticmethod
	def init():
		mts.MapTemporarySave.init()
		mp.MapRender.init()
		MapManager.changeValues = ["null", "map0", 0]
		MapManager.zone = "null"
		MapManager.id = "null"
		MapManager.entry = -1

		MapManager.transition = False
		MapManager.transitionPhase = 0
		MapManager.transitionCount = 0

		MapManager.collideTest = True

		# Force to load the first map with transition
		MapManager.reserveChange("intro", "hall", 0)
		MapManager.checkChangeMap()
		MapManager.transitionPhase = 1

	@staticmethod
	def reserveChange(zone, map, entry, exitPos=4):
		MapManager.changeValues = [zone, map, entry]
		if exitPos == 4:
			MapManager.exitPos = 4
		else:
			MapManager.exitPos = mts.MapTemporarySave.getExitTransition(zone, map, entry)

	@staticmethod
	# Change one bloc of the interaction map
	def setTile(position, id):
		MapManager.interaction[MapManager.iHeight - 1 - math.floor(position[1])][math.floor(position[0])] = id

		# Check if entity with collision in the change
		if id == MapManager.INTERACTION_SOLID and MapManager.collideTest:
			for i in em.EntityManager.entitiesCol:

				if not em.EntityManager.entities[i.id].attributes["collision"] == 0:
					e = em.EntityManager.entities[i.id]
					# Collision Test
					if math.floor(e.pos[0] * MapManager.COEF - e.halfColSize[0] * MapManager.COEF) <= position[
						0] <= math.floor(
						e.pos[0] * MapManager.COEF + e.halfColSize[0] * MapManager.COEF) and \
							math.floor(e.pos[1] * MapManager.COEF - e.halfColSize[1] * MapManager.COEF) <= position[
						1] <= math.floor(
						e.pos[1] * MapManager.COEF + e.halfColSize[1] * MapManager.COEF):

						if not e.type == "Player":
							em.EntityManager.remove(e.id, e.type)
						else:
							e.applyDamage(1)
							e.setPos(MapManager.entryInfo[0])
							e.setSpeed([0, 0])

	# Set a new id for a tile
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

	# MapTemporarySave send values to apply during the map changing
	@staticmethod
	def setupMapValues(interaction, defaultEntry, entryInfo):
		MapManager.interaction = interaction
		MapManager.defaultEntry = defaultEntry

		# Set the size of the current map
		iWidth = len(MapManager.interaction[0])
		iHeight = len(MapManager.interaction)
		MapManager.iWidth = iWidth
		MapManager.iHeight = iHeight

		# Create instance of entities and place players
		MapManager.entryInfo = entryInfo
		e1 = em.EntityManager.entities[em.EntityManager.PLAYER_1]
		e2 = em.EntityManager.entities[em.EntityManager.PLAYER_2]

		# Difference places for according to the entry direction
		if entryInfo[1] == "left":
			e1.setPos([entryInfo[0][0], entryInfo[0][1] + 0.5])
			e2.setPos([entryInfo[0][0], entryInfo[0][1] - 0.5])
			e1.setDirection(0)
			e2.setDirection(0)
		elif entryInfo[1] == "right":
			e1.setPos([entryInfo[0][0], entryInfo[0][1] + 0.5])
			e2.setPos([entryInfo[0][0], entryInfo[0][1] - 0.5])
			e1.setDirection(2)
			e2.setDirection(2)
		elif entryInfo[1] == "up":
			e1.setPos([entryInfo[0][0] - 0.5, entryInfo[0][1]])
			e2.setPos([entryInfo[0][0] + 0.5, entryInfo[0][1]])
			e1.setDirection(1)
			e2.setDirection(1)
		elif entryInfo[1] == "down":
			e1.setPos([entryInfo[0][0] - 0.5, entryInfo[0][1]])
			e2.setPos([entryInfo[0][0] + 0.5, entryInfo[0][1]])
			e1.setDirection(3)
			e2.setDirection(3)
		else:
			e1.setPos(entryInfo[0])
			e2.setPos(entryInfo[0])
			e1.setDirection(3)
			e2.setDirection(3)

		e1.speed = [0, 0]
		e2.speed = [0, 0]

	@staticmethod
	def unload():
		mp.MapRender.unload()
		mts.MapTemporarySave.unloadAll()

	@staticmethod
	def update():
		if MapManager.transition:
			# End of transition
			if MapManager.transitionPhase > 2:
				# Reset values
				MapManager.transitionCount = 0
				MapManager.transitionPhase = 0
				gm.GameManager.currentScreen.mapChange = False
				MapManager.transition = False

				# Put the transition texture in Petaouchnoque
				mp.MapRender.setTransitionPos([999999, 999999])
			# In a phase
			else:
				# If end of each phase
				if MapManager.transitionCount >= MapManager.TRANSITION_TIMES[MapManager.transitionPhase]:
					MapManager.transitionPhase += 1
					MapManager.transitionCount = 0
				# Update during the transition
				else:
					# Begin
					if MapManager.transitionPhase == MapManager.TRANSITION_BEGIN:
						pos = gm.GameManager.cam.pos.copy()
						# Pos take in consideration the position of camera
						pos[0] = 9
						pos[1] = 6
						if MapManager.exitPos == 1:
							pos[1] += mathcda.map(MapManager.transitionCount - 0.001, 0,
												  MapManager.TRANSITION_TIMES[
													  MapManager.transitionPhase], 0, 12) - 12
						elif MapManager.exitPos == 3:
							pos[1] += - mathcda.map(MapManager.transitionCount - 0.001, 0,
													MapManager.TRANSITION_TIMES[
													   MapManager.transitionPhase], 0, 12) + 12
						elif MapManager.exitPos == 0:
							pos[0] += - mathcda.map(MapManager.transitionCount - 0.001, 0,
													MapManager.TRANSITION_TIMES[
													   MapManager.transitionPhase], 0, 18) + 18
						elif MapManager.exitPos == 2:
							pos[0] += mathcda.map(MapManager.transitionCount - 0.001, 0,
												  MapManager.TRANSITION_TIMES[
													  MapManager.transitionPhase], 0, 18) - 18

						mp.MapRender.setTransitionPos(pos)
					# End
					elif MapManager.transitionPhase == MapManager.TRANSITION_END:
						pos = gm.GameManager.cam.pos.copy()
						pos[0] = 9
						pos[1] = 6
						if MapManager.exitPos == 1:
							pos[1] += mathcda.map(MapManager.transitionCount - 0.001, 0,
												  MapManager.TRANSITION_TIMES[
													  MapManager.transitionPhase], 12, 0) - 12
						elif MapManager.exitPos == 3:
							pos[1] += - mathcda.map(MapManager.transitionCount - 0.001, 0,
													MapManager.TRANSITION_TIMES[
													   MapManager.transitionPhase], 12, 0) + 12
						elif MapManager.exitPos == 0:
							pos[0] += - mathcda.map(MapManager.transitionCount - 0.001, 0,
													MapManager.TRANSITION_TIMES[
													   MapManager.transitionPhase], 18, 0) + 18
						elif MapManager.exitPos == 2:
							pos[0] += mathcda.map(MapManager.transitionCount - 0.001, 0,
												  MapManager.TRANSITION_TIMES[
													  MapManager.transitionPhase], 18, 0) - 18
						mp.MapRender.setTransitionPos(pos)
					# Load the new map
					elif MapManager.transitionPhase == MapManager.TRANSITION_LOAD:
						if MapManager.transitionCount == 0:
							if MapManager.exitPos <= 3:
								MapManager.exitPos = (MapManager.exitPos + 2) % 4

							MapManager.changeRoom()
							pos = gm.GameManager.cam.pos.copy()
							pos[0] = 9
							pos[1] = 6
							mp.MapRender.setTransitionPos(pos)

					MapManager.transitionCount += 1

		else:
			ev.dispose()
			MapManager.checkChangeMap()
			mp.MapRender.dispose()
