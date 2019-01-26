# This class performs the display and the update of the client

from game.screen.screens import screen
from game.render.texture import texture
from game.render.shape import shape
from game.render.shader import gluniforms as glU
from game.screen import gamemanager as gameManager
from game.inputs import keyboardmanager as key

import pyrr
import glfw


class GameScreen(screen.Screen):
	
	def __init__(self):
		super(GameScreen, self).__init__()
		width = 18
		height = 12

		quad = [-width/2, -height/2, 0.0,  0.0, 0.0,
				width/2, -height/2, 0.0,  1.0, 0.0,
				width/2, height/2, 0.0,  1.0, 1.0,
				-width/2, height/2, 0.0,  0.0, 1.0]

		indices = [0, 1, 2,
					2, 3, 0]
		self.shape = shape.Shape("texVert.glsl", "texFrag.glsl")
		self.shape.setEbo(indices)
		self.shape.setVertices(quad, [3, 2])

		self.tex = texture.Texture("map1")
		from game.render import mapfunctions as mapFunctions
		self.tex.loadImage(mapFunctions.createMap(width, height, 32))

		self.tex.bind()
		self.shape.shader.addLink("model")
		self.modelMtx = pyrr.Matrix44.identity()
		glU.glUniformv(self.shape.shader, "model", self.modelMtx)

	def update(self):
		if key.getKey(glfw.KEY_Z) == 1:	
			gameManager.GameManager.cam.addPos([0.0, 0.0, +0.01])
		
		if key.getKey(glfw.KEY_P) == 1:	
			print(gameManager.GameManager.cam.camPos[2])

	def display(self):
		self.shape.applyShader()
		self.shape.bind()
		self.shape.view()

		self.shape.draw()

	def unload(self):
		self.shape.unload()
		self.tex.unload()
