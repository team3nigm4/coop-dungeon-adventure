import json

from game.render.shape import shape
from game.game.map import mapmanager as mp
from game.render.texture import texture
from game.util import matrix4f
from game.render.shader.shadermanager import ShaderManager as sm

class MapRender:
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
	vboCount = 0
	ebo = []
	eboCount = 0
	floorVbo = [0,0,0,0,0,0,0,0]

	modelDown =  matrix4f.Matrix4f()

	change = False

	@staticmethod
	def init():
		path_tileSetImage = "/tiles/tileset.png"
		path_tileSet = "game/resources/textures/tiles/tileset.json"
		MapRender.tileSet = json.load(open(path_tileSet))
		MapRender.tileSetImage = texture.Texture(path_tileSetImage)
		MapRender.tileSetImage.load()

		MapRender.shapeUp = shape.Shape("texture", True)
		MapRender.shapeDown = shape.Shape("texture", True)

		MapRender.modelDown = matrix4f.Matrix4f(True)
		sm.updateLink("texture", "model", MapRender.modelDown.matrix)

	@staticmethod
	def constructMap():
		y = len(MapRender.mapValues[0])
		x = len(MapRender.mapValues[0][0])
		MapRender.tilesPosition = [[[None for jk in range(x)] for kj in range(y)] for lk in range(2)]

		MapRender.vbo = []
		MapRender.ebo = []
		MapRender.eboCount = 0
		MapRender.vboCount = 0

		for floor in range(2):
			for height in range(len(MapRender.mapValues[floor])):
				for width in range(len(MapRender.mapValues[floor][height])):
					id = MapRender.mapValues[floor][height][width]
					if id != 0:
						pos = MapRender.tileSet["textPos"][MapRender.tileSet["id"][id - 1]]
						MapRender.addTile(floor, width, y - height, pos[0], pos[1])

		MapRender.shapeDown.setVertices(MapRender.vbo, [3, 2], MapRender.ebo)

	@staticmethod
	def display():
		sm.updateLink("texture", "model", MapRender.modelDown.matrix)
		MapRender.tileSetImage.bind()
		MapRender.shapeDown.bind()
		MapRender.shapeDown.draw()

	@staticmethod
	def dispose():
		if MapRender.change:
			MapRender.shapeDown.resetVBO(MapRender.vbo)
			MapRender.change = False

	@staticmethod
	def addTile(floor, posX, posY, tposX, tposY, rotate=1):
		if MapRender.tilesPosition[floor][mp.MapManager.height - posY][posX] is None:
			eboIndex = MapRender.eboCount * 4

			MapRender.ebo.append(eboIndex)
			MapRender.ebo.append(eboIndex + 1)
			MapRender.ebo.append(eboIndex + 3)
			MapRender.ebo.append(eboIndex + 1)
			MapRender.ebo.append(eboIndex + 2)
			MapRender.ebo.append(eboIndex + 3)

			MapRender.eboCount +=1

		vboCount = MapRender.vboCount * 20
		MapRender.tilesPosition[floor][mp.MapManager.height - posY][posX] = MapRender.vboCount
		MapRender.vboCount += 1

		if rotate == 0:
			MapRender.addPos(posX, posY - 1,
							 tposX, tposY, vboCount)

			MapRender.addPos(posX + 1, posY - 1,
							 tposX, tposY + 1, vboCount)

			MapRender.addPos(posX + 1, posY,
							 tposX + 1, tposY + 1, vboCount)

			MapRender.addPos(posX, posY,
							 tposX + 1, tposY, vboCount)
		elif rotate == 2:
			MapRender.addPos(posX, posY - 1,
							 tposX + 1, tposY + 1, vboCount)

			MapRender.addPos(posX + 1, posY - 1,
							 tposX + 1, tposY, vboCount)

			MapRender.addPos(posX + 1, posY,
							 tposX, tposY, vboCount)

			MapRender.addPos(posX, posY,
							 tposX, tposY + 1, vboCount)
		elif rotate == 1:
			MapRender.addPos(posX, posY - 1,
							 tposX, tposY + 1, vboCount)

			MapRender.addPos(posX + 1, posY - 1,
							 tposX + 1, tposY + 1, vboCount)

			MapRender.addPos(posX + 1, posY,
							 tposX + 1, tposY, vboCount)

			MapRender.addPos(posX, posY,
							 tposX, tposY, vboCount)
		elif rotate == 3:
			MapRender.addPos(posX, posY - 1,
							 tposX + 1, tposY, vboCount)

			MapRender.addPos(posX + 1, posY - 1,
							 tposX, tposY, vboCount)

			MapRender.addPos(posX + 1, posY,
							 tposX, tposY + 1, vboCount)

			MapRender.addPos(posX, posY,
							 tposX + 1, tposY + 1, vboCount)
		MapRender.change = True

	@staticmethod
	def addPos(posX, posY, tposX, tposY, vboPos):
		MapRender.vbo.insert(vboPos, float(posX))
		MapRender.vbo.insert(vboPos + 1, float(posY))
		MapRender.vbo.insert(vboPos + 2, 0.0)
		MapRender.vbo.insert(vboPos + 3, round(tposX / MapRender.tileSet["info"]["size"][0], 3))
		MapRender.vbo.insert(vboPos + 4,
							 MapRender.tileSet["info"]["size"][1] - round(tposY / MapRender.tileSet["info"]["size"][1],
																		  3))

	@staticmethod
	def deleteTile(layer, posX, posY):
		vbo = MapRender.tilesPosition[layer][mp.MapManager.height - posY][posX]
		MapRender.tilesPosition[layer][mp.MapManager.height - posY][posX] = None
		for i in range(20):
			del MapRender.vbo[vbo*20]
		for i in range(6):
			del MapRender.ebo[len(MapRender.ebo) - 1]

		MapRender.change = True

	@staticmethod
	def unload():
		MapRender.shapeDown.unload()
		MapRender.shapeUp.unload()
		MapRender.tileSetImage.unload()
