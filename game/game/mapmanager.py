# Manages the current map, displays it, and performs various actions on it (collision test)

import math

import pyrr

from game.game.entitymanager import EntityManager as em
from game.render.shader.shadermanager import ShaderManager as sm
from game.render.shape import shape
from game.render.texture import texture
from game.screen.gamemanager import GameManager as gm


class MapManager:
	width = None
	height = None
	shape = None
	modelMtx = None
	tex = [None]
	collision = [None]

	@staticmethod
	def init():
		MapManager.shape = shape.Shape(0)

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

	@staticmethod
	def checkCollisionX(position, speed, colBoxSize):
		half = colBoxSize / 2
		nextPos = position[0] + speed
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.width:
			posY = [math.floor(position[1] - half), math.floor(position[1] + half)]

			if speed > 0:
				nextPos = math.floor(nextPos + half)
				if MapManager.collision[MapManager.height - 1 - posY[0]][nextPos] == 1 or \
						MapManager.collision[MapManager.height - 1 - posY[1]][nextPos] == 1:
					return nextPos - half - 0.001
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.collision[MapManager.height - 1 - posY[0]][nextPos] == 1 or \
						MapManager.collision[MapManager.height - 1 - posY[1]][nextPos] == 1:
					return nextPos + 1 + half + 0.001
		else:
			return position[0]
		return position[0] + speed

	@staticmethod
	def checkCollisionY(position, speed, colBoxSize):
		half = colBoxSize / 2
		nextPos = position[1] + speed
		if math.floor(nextPos - half) >= 0 and math.floor(nextPos + half) < MapManager.height:
			posX = [math.floor(position[0] - half), math.floor(position[0] + half)]

			if speed > 0:
				nextPos = math.floor(nextPos + half)
				if MapManager.collision[MapManager.height - 1 - nextPos][posX[0]] == 1 or \
						MapManager.collision[MapManager.height - 1 - nextPos][posX[1]] == 1:
					return nextPos - half - 0.001
			else:
				nextPos = math.floor(nextPos - half)
				if MapManager.collision[MapManager.height - 1 - nextPos][posX[0]] == 1 or \
						MapManager.collision[MapManager.height - 1 - nextPos][posX[1]] == 1:
					return nextPos + 1 + half + 0.001
		else:
			return position[1]
		return position[1] + speed

	@staticmethod
	def changeRoom():
		# Clear the game before changing
		em.clear()
		from game.game import mapfunctions

		# Load new room
		values = mapfunctions.createMap()
		width = values[0][0]
		height = values[0][1]

		MapManager.collision = values[2]

		quad = [0, 0, 0.0, 0.0, 0.0,
				width, 0, 0.0, 1.0, 0.0,
				width, height, 0.0, 1.0, 1.0,
				0, height, 0.0, 0.0, 1.0]

		if width <= 18 and height <= 12:
			gm.cam.setPos([0, 0, gm.cam.camPos[2]])
			gm.cam.addPos([-width / 2, -height / 2, 0])

		sm.updateLink(sm.TEXTURE, "view", gm.cam.getView())

		indices = [0, 1, 2,
					2, 3, 0]

		MapManager.shape.setEbo(indices)
		MapManager.shape.setVertices(quad, [3, 2])

		MapManager.tex = [None] * len(values[3])
		for i in range(0, len(values[3])):
			MapManager.tex[i] = texture.Texture("map1")
			MapManager.tex[i].loadImage(values[3][i])

		em.entities[em.PLAYER_1].setPos(values[1])

		MapManager.width = width
		MapManager.height = height

	@staticmethod
	def unload():
		MapManager.shape.unload()
		for i in range(0, len(MapManager.tex)):
			MapManager.tex[i].unload()
