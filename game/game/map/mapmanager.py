# Manages the current map, displays it, and performs various actions on it (collision test)

import math

import pyrr

from game.game.entityclass.entitymanager import EntityManager as em
from game.render.shader.shadermanager import ShaderManager as sm
from game.render.shape import shape
from game.render.texture import texture
from game.screen.gamemanager import GameManager as gm


class MapManager:

	DATA_MAP_INFO = 0
	DATA_IMAGES = 1
	DATA_INTERACTIONS = 2
	DATA_ENTRIES = 3
	DATA_ENTITIES = 4

	INTERACTION_SOLID = 1

	width = None
	height = None
	shape = None
	modelMtx = None
	tex = []
	interaction = []

	zone = "null"
	id = "null"
	defaultEntry = 0

	changeValues = None

	@staticmethod
	def init():

		quad = [0.0, 0.0, 0.0, 0.0, 0.0,
				1.0, 0.0, 0.0, 1.0, 0.0,
				1.0, 1.0, 0.0, 1.0, 1.0,
				0.0, 1.0, 0.0, 0.0, 1.0]

		indices = [0, 1, 2,
				   2, 3, 0]

		MapManager.shape = shape.Shape(0, True)
		MapManager.shape.setVertices(quad, [3, 2], indices)

		MapManager.modelMtx = pyrr.Matrix44.identity()
		sm.updateLink(sm.TEXTURE, "model", MapManager.modelMtx)

		gm.cam.trackEntity(em.PLAYER_1)

		MapManager.changeRoom("test", "map1", 0)

	@staticmethod
	def display():
		sm.updateLink(sm.TEXTURE, "model", MapManager.modelMtx)
		MapManager.shape.applyShader()
		MapManager.shape.bind()

		for i in range(0, len(MapManager.tex)):
			MapManager.tex[i].bind()
			MapManager.shape.draw()
		MapManager.shape.unbind()

	@staticmethod
	def checkCollisionX(position, speed, colBoxSize):
		half = colBoxSize[0]
		nextPos = position[0] + speed
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.width:
			posY = [math.floor(position[1] - colBoxSize[1]), math.floor(position[1] + colBoxSize[1])]

			if speed > 0:
				nextPos = math.floor(nextPos + half)
				if MapManager.interaction[MapManager.height - 1 - posY[0]][nextPos] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.height - 1 - posY[1]][
							nextPos] == MapManager.INTERACTION_SOLID:
					return nextPos - half - 0.001
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.interaction[MapManager.height - 1 - posY[0]][nextPos] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.height - 1 - posY[1]][
							nextPos] == MapManager.INTERACTION_SOLID:
					return nextPos + 1 + half + 0.001
		else:
			return position[0]
		return position[0] + speed

	@staticmethod
	def checkCollisionY(position, speed, colBoxSize):
		half = colBoxSize[1]
		nextPos = position[1] + speed
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.height:
			posX = [math.floor(position[0] - colBoxSize[0]), math.floor(position[0] + colBoxSize[0])]

			if speed > 0:
				nextPos = math.floor(nextPos + half)
				if MapManager.interaction[MapManager.height - 1 - nextPos][posX[0]] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.height - 1 - nextPos][
							posX[1]] == MapManager.INTERACTION_SOLID:
					return nextPos - half - 0.001
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.interaction[MapManager.height - 1 - nextPos][posX[0]] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.height - 1 - nextPos][
							posX[1]] == MapManager.INTERACTION_SOLID:
					return nextPos + 1 + half + 0.001
		else:
			return position[1]
		return position[1] + speed

	@staticmethod
	def changeRoom(zone, map, entry):
		# Clear the game before changing
		em.clear()
		MapManager.changeValues = None

		# Load new room
		from game.game.map import mapfunctions
		values = mapfunctions.loadMap(zone, map, entry)

		# Apply values
		MapManager.zone = values[MapManager.DATA_MAP_INFO][0]
		MapManager.id = values[MapManager.DATA_MAP_INFO][1]
		MapManager.defaultEntry = values[MapManager.DATA_MAP_INFO][2]

		for i in range(0, len(values[MapManager.DATA_IMAGES])):
			MapManager.tex.append(texture.Texture("map1"))
			len(MapManager.tex)
			MapManager.tex[i].loadImage(values[MapManager.DATA_IMAGES][i])

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
		em.entities[em.PLAYER_1].setPos(values[MapManager.DATA_ENTRIES])

		from game.game.map import loadentity
		for i in range(0, len(values[MapManager.DATA_ENTITIES])):
			em.add(loadentity.LoadEntity.instance(values[MapManager.DATA_ENTITIES][str(i)]))

		# Work with values
		quad = [0, 0, 0.0, 0.0, 0.0,
				width, 0, 0.0, 1.0, 0.0,
				width, height, 0.0, 1.0, 1.0,
				0, height, 0.0, 0.0, 1.0]

		MapManager.shape.resetVBO(quad)

		# Set the camera position
		gm.cam.setPos([0, 0, gm.cam.pos[2]])

		if width > 18:
			gm.cam.track[0] = True
		else:
			gm.cam.track[0] = False
			gm.cam.addPos([-width / 2, 0 , 0])

		if height > 12:
			gm.cam.track[1] = True
		else:
			gm.cam.track[1] = False
			gm.cam.addPos([0, -height / 2, 0])	

		gm.cam.goToEntity()
		sm.updateLink(sm.TEXTURE, "view", gm.cam.getView())
		

	@staticmethod
	def unload():
		MapManager.shape.unload()
		MapManager.unloadImages()

	@staticmethod
	# Change one bloc of the interaction map
	def changeInterMap(position, id):
		MapManager.interaction[MapManager.height - 1 - math.floor(position[1])][math.floor(position[0])] = id

	# Change a zone of the interaction map
	@staticmethod
	def changeInterMapSize(position, size,  id):
		posX = [math.floor(position[0] - size[0]), math.floor(position[0] + size[0])]
		posY = [math.floor(position[1] - size[1]), math.floor(position[1] + size[1])]

		for x in range(posX[0], posX[1]+1):
			for y in range(posY[0], posY[1]+1):
				MapManager.interaction[MapManager.height - 1 - y][x] = id

	@staticmethod
	def reserveChange(values):
		MapManager.changeValues = values

	@staticmethod
	def checkChangeMap():
		if not MapManager.changeValues == None:
			MapManager.unloadImages()
			MapManager.changeRoom(MapManager.changeValues[0], MapManager.changeValues[1], MapManager.changeValues[2])


	@staticmethod
	def unloadImages():
		for i in range(0, len(MapManager.tex)):
			MapManager.tex[i].unload()
		MapManager.tex = []
