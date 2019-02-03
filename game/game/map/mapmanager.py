# Manages the current map, displays it, and performs various actions on it (collision test)

import math

import pyrr

from game.game.entityclass.entitymanager import EntityManager as em
from game.render.shader.shadermanager import ShaderManager as sm
from game.render.shape import shape
from game.render.texture import texture
from game.screen.gamemanager import GameManager as gm


class MapManager:
	width = None
	height = None
	shape = None
	modelMtx = None
	tex = []
	interaction = []
	id = "null"

	DATA_MAP_ID = 0
	DATA_IMAGES = 1
	DATA_INTERACTIONS = 2
	DATA_ENTRIES = 3
	DATA_ENTITIES = 4

	INTERACTION_SOLID = 1

	@staticmethod
	def init():

		quad = [0.0, 0.0, 0.0, 		0.0, 0.0,
				1.0, 0.0, 0.0, 		1.0, 0.0,
				1.0, 1.0, 0.0, 		1.0, 1.0,
				0.0, 1.0, 0.0, 		0.0, 1.0]

		indices = [0, 1, 2,
				   2, 3, 0]

		MapManager.shape = shape.Shape(0, True)
		MapManager.shape.setVertices(quad, [3, 2], indices)

		MapManager.modelMtx = pyrr.Matrix44.identity()
		sm.updateLink(sm.TEXTURE, "model", MapManager.modelMtx)
		MapManager.changeRoom()

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
						MapManager.interaction[MapManager.height - 1 - posY[1]][nextPos] == MapManager.INTERACTION_SOLID:
					return nextPos - half - 0.001
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.interaction[MapManager.height - 1 - posY[0]][nextPos] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.height - 1 - posY[1]][nextPos] == MapManager.INTERACTION_SOLID:
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
						MapManager.interaction[MapManager.height - 1 - nextPos][posX[1]] == MapManager.INTERACTION_SOLID:
					return nextPos - half - 0.001
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.interaction[MapManager.height - 1 - nextPos][posX[0]] == MapManager.INTERACTION_SOLID or \
						MapManager.interaction[MapManager.height - 1 - nextPos][posX[1]] == MapManager.INTERACTION_SOLID:
					return nextPos + 1 + half + 0.001
		else:
			return position[1]
		return position[1] + speed

	@staticmethod
	def changeRoom():
		# Clear the game before changing
		em.clear()

		# Load new room
		from game.game.map import mapfunctions
		values = mapfunctions.createMap()

		# Apply values

		MapManager.id = values[MapManager.DATA_MAP_ID]

		for i in range(0, len(values[MapManager.DATA_IMAGES])):
			MapManager.tex.append(texture.Texture("map1"))
			len(MapManager.tex)
			MapManager.tex[i].loadImage(values[MapManager.DATA_IMAGES][i])

		MapManager.interaction = values[MapManager.DATA_INTERACTIONS]

		em.entities[em.PLAYER_1].setPos(values[MapManager.DATA_ENTRIES])

		# Add test entity
		from game.game.entitymodel import slidingblock
		entity1 = slidingblock.SlidingBlock(["SlidingBlock", [10.5, 7.5]])
		em.add(entity1)

		from game.game.entitymodel import pressureplate
		entity2 = pressureplate.PressurePlate(["PressurePlate", [8.5, 8.5]])
		em.add(entity2)

		width = len(MapManager.interaction[0])
		height = len(MapManager.interaction)

		# Work with values

		quad = [0, 0, 0.0, 				0.0, 0.0,
				width, 0, 0.0, 			1.0, 0.0,
				width, height, 0.0, 	1.0, 1.0,
				0, height, 0.0, 		0.0, 1.0]

		MapManager.shape.resetVBO(quad)

		# Set the camera position
		if width <= 18 and height <= 12:
			gm.cam.setPos([0, 0, gm.cam.camPos[2]])
			gm.cam.addPos([-width / 2, -height / 2, 0])
		sm.updateLink(sm.TEXTURE, "view", gm.cam.getView())

		MapManager.width = width
		MapManager.height = height

	@staticmethod
	def unload():
		MapManager.shape.unload()
		MapManager.unloadImages()

	@staticmethod
	def setInteractionBloc(position, id):
		MapManager.interaction[MapManager.height - 1 - math.floor(position[1])][math.floor(position[0])] = id


	@staticmethod
	def unloadImages():
		for i in range(0, len(MapManager.tex)):
			MapManager.tex[i].unload()
		MapManager.tex = []