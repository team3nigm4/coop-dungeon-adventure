# This class performs the display and the update of the client

from game.screen.screens import screen
from game.render.texture import texture
from game.render.shape import shape
from game.screen.gamemanager import GameManager
from game.inputs.inputmanager import InputManager as im
from game.game.entitymanager import EntityManager as em
from game.render.shader.shadermanager import ShaderManager as sm
from game.game import player as pl

import pyrr
import time

class GameScreen(screen.Screen):

	def __init__(self):
		super(GameScreen, self).__init__()
		self.shape = None
		self.tex = None

		em.init()

		player = pl.Player(["Player", [0,0], [1,1], "perso.png"])
		em.add(player)

		self.shape = shape.Shape(0)

		self.modelMtx = pyrr.Matrix44.identity()
		sm.updateLink(sm.TEXTURE, "model", self.modelMtx)
		self.changeRoom()

	def update(self):
		# Receive and create data
		serverData = GameManager.serverData
		clientData = im.getState()

		if im.inputPressed(im.RESET):
			self.unload()
			self.changeRoom()

		em.update()

		# Return data
		clientData.append(time.time_ns())
		GameManager.clientData = clientData

	def display(self):
		sm.updateLink(sm.TEXTURE, "model", self.modelMtx)
		self.shape.applyShader()
		self.shape.bind()

		for i in range(0, len(self.tex)):
			self.tex[i].bind()
			self.shape.draw()

		em.display()

	def changeRoom(self):
		# Clear the game before changing
		em.clear()

		# Load new room
		from game.render import mapfunctions as mapFunctions
		values = mapFunctions.createMap()
		width = values[0][0]
		height = values[0][1]

		self.collision = values[2]

		quad = [-width / 2, -height / 2, 0.0, 0.0, 0.0,
				width / 2, -height / 2, 0.0, 1.0, 0.0,
				width / 2, height / 2, 0.0, 1.0, 1.0,
				-width / 2, height / 2, 0.0, 0.0, 1.0]

		indices = [0, 1, 2,
				   2, 3, 0]

		self.shape.setEbo(indices)
		self.shape.setVertices(quad, [3, 2])

		self.tex = [None] * len(values[3])
		for i in range(0, len(values[3])):
			self.tex[i] = texture.Texture("map1")
			self.tex[i].loadImage(values[3][i])

		em.entities[em.PLAYER_1].setPos(values[1])

	def unload(self):
		self.shape.unload()
		for i in range(0, len(self.tex)):
			self.tex[i].unload()
		em.unload()
