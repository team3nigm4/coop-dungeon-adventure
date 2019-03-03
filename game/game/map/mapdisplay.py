import json

from game.render.shape import shape
from game.game.map import mapmanager as mp
from game.render.texture import texture
from game.util import matrix4f
from game.render.shader.shadermanager import ShaderManager as sm

class MapDisplay:

	GROUND = 0
	GROUND2 = 1
	BASE_WALL = 2
	BASE_WALL2 = 3
	HIGH_WALL = 4
	HIGH_WALL2 = 5
	SUPP = 6
	SUPP2 = 7

	tileSetImage = None
	tileSet = None

	shapeUp = None
	shapeDown = None

	mapValues = []
	tilesPosition = []

	vbo = []
	ebo = []

	modelDown =  matrix4f.Matrix4f()

	@staticmethod
	def init():
		path_tileSetImage = "/tiles/tileset.png"
		path_tileSet = "game/resources/textures/tiles/tileset.json"
		MapDisplay.tileSet = json.load(open(path_tileSet))
		MapDisplay.tileSetImage = texture.Texture(path_tileSetImage)
		MapDisplay.tileSetImage.load()

		MapDisplay.shapeUp = shape.Shape("texture", True)
		MapDisplay.shapeDown = shape.Shape("texture", True)

		MapDisplay.modelDown = matrix4f.Matrix4f(True)
		sm.updateLink("texture", "model", MapDisplay.modelDown.matrix)

	@staticmethod
	def constructMap():
		MapDisplay.tilesPosition = []
		MapDisplay.vbo = []
		MapDisplay.ebo = []
		gap = MapDisplay.tileSet["info"]["gap"]
		size = MapDisplay.tileSet["info"]
		count = 0
		for step in range(2):
			y = len(MapDisplay.mapValues[step])
			for height in range(len(MapDisplay.mapValues[step])):
				for width in range(len(MapDisplay.mapValues[step][height])):
					id = MapDisplay.mapValues[step][height][width]
					if id != 0:
						pos = MapDisplay.tileSet["textPos"][MapDisplay.tileSet["id"][id - 1]]

						MapDisplay.addBlock(width, y - height-1,
											pos[0], pos[1])

						MapDisplay.addBlock(width + 1, y - height-1,
											pos[0] + 1, pos[1])

						MapDisplay.addBlock(width + 1, y - height,
											pos[0] + 1, pos[1] + 1)

						MapDisplay.addBlock(width, y - height,
											pos[0], pos[1] + 1)

						MapDisplay.ebo.append(count)
						MapDisplay.ebo.append(count + 1)
						MapDisplay.ebo.append(count + 3)
						MapDisplay.ebo.append(count + 1)
						MapDisplay.ebo.append(count + 2)
						MapDisplay.ebo.append(count + 3)
						count += 4

		print(MapDisplay.vbo)
		print(MapDisplay.ebo)
		MapDisplay.shapeDown.setVertices(MapDisplay.vbo, [3, 2], MapDisplay.ebo)

	@staticmethod
	def display():
		sm.updateLink("texture", "model", MapDisplay.modelDown.matrix)
		MapDisplay.tileSetImage.bind()
		MapDisplay.shapeDown.bind()
		MapDisplay.shapeDown.draw()


	@staticmethod
	def addBlock(width, height, posX, posY):
		MapDisplay.vbo.append(float(width))
		MapDisplay.vbo.append(float(height))
		MapDisplay.vbo.append(0.0)
		MapDisplay.vbo.append(round(posX / MapDisplay.tileSet["info"]["size"][0], 3))
		MapDisplay.vbo.append(round(posY / MapDisplay.tileSet["info"]["size"][1], 3))

	@staticmethod
	def unload():
		MapDisplay.shapeDown.unload()
		MapDisplay.shapeUp.unload()
		MapDisplay.tileSetImage.unload()
