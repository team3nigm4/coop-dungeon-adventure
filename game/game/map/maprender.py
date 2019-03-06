import json

from game.render.shape import shape
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

	tWidth = 0
	tHeight = 0

	shapeUp = None
	shapeDown = None

	mapValues = []
	tilesPosition = []

	vbo = []
	vboCount = 0
	ebo = []
	eboCount = 0
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
		MapRender.shapeUp.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		MapRender.shapeUp.setReading([3, 2])
		MapRender.shapeDown = shape.Shape("texture", True)
		MapRender.shapeDown.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		MapRender.shapeDown.setReading([3, 2])

		MapRender.modelDown = matrix4f.Matrix4f(True)
		sm.updateLink("texture", "model", MapRender.modelDown.matrix)

	@staticmethod
	def constructMap():
		height = len(MapRender.mapValues[0])
		width = len(MapRender.mapValues[0][0])
		MapRender.tWidth = width
		MapRender.tHeight = height

		MapRender.tilesPosition = [[[None for jk in range(width)] for kj in range(height)] for lk in range(2)]

		MapRender.vbo = []
		MapRender.ebo = []
		MapRender.eboCount = 0
		MapRender.vboCount = 0

		for floor in range(2):
			for y in range(len(MapRender.mapValues[floor])):
				for x in range(len(MapRender.mapValues[floor][y])):
					id = MapRender.mapValues[floor][y][x]
					if id != 0:
						pos = MapRender.tileSet["textPos"][MapRender.tileSet["id"][id - 1]]
						MapRender.addTile2(MapRender.vboCount, floor, x, height - y - 1, pos[0], pos[1])
						MapRender.vboCount += 1

		MapRender.change = True
		MapRender.dispose()

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
	def display():
		sm.updateLink("texture", "model", MapRender.modelDown.matrix)
		MapRender.tileSetImage.bind()
		MapRender.shapeDown.bind()
		MapRender.shapeDown.draw()

	@staticmethod
	def dispose():
		if MapRender.change:
			MapRender.shapeDown.setEbo(MapRender.ebo)
			MapRender.shapeDown.setVbo(MapRender.vbo)
			MapRender.change = False

	@staticmethod
	def addTile(floor, posX, posY, textName, rotate=1):
		vboCount = MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX]
		if vboCount is None:
			vboCount = MapRender.reserveNextVbo(floor, posX, posY)
		else: 
			MapRender.deleteTile(floor, posX, posY)
			MapRender.shiftVboIndex(floor, posX, posY)

		pos = MapRender.tileSet["textPos"][textName]
		MapRender.addTile2(vboCount, floor, posX, posY, pos[0], pos[1], rotate)
		MapRender.change = True

	@staticmethod
	def addTile2(vboCount, floor, posX, posY, tposX, tposY, rotate=1):
		eboIndex = MapRender.eboCount * 4

		MapRender.ebo.append(eboIndex)
		MapRender.ebo.append(eboIndex + 1)
		MapRender.ebo.append(eboIndex + 3)
		MapRender.ebo.append(eboIndex + 1)
		MapRender.ebo.append(eboIndex + 2)
		MapRender.ebo.append(eboIndex + 3)

		MapRender.eboCount +=1

		MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX] = vboCount	

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

	@staticmethod
	def addPos(posX, posY, tposX, tposY, vboPos):
		vboPos *= 20
		posY += 1
		MapRender.vbo.insert(vboPos, float(posX))
		MapRender.vbo.insert(vboPos + 1, float(posY))
		MapRender.vbo.insert(vboPos + 2, 0.0)
		MapRender.vbo.insert(vboPos + 3, round(tposX / MapRender.tileSet["info"]["size"][0], 3))
		MapRender.vbo.insert(vboPos + 4,
							 MapRender.tileSet["info"]["size"][1] - round(tposY / MapRender.tileSet["info"]["size"][1], 3))

	@staticmethod
	def deleteTile(layer, posX, posY):
		vbo = MapRender.tilesPosition[layer][MapRender.tHeight - posY - 1][posX]
		if not vbo == None:
			MapRender.tilesPosition[layer][MapRender.tHeight - posY - 1][posX] = None
			for i in range(20):
				del MapRender.vbo[vbo*20]
			for i in range(6):
				del MapRender.ebo[len(MapRender.ebo) - 1]
			MapRender.eboCount -=1

			MapRender.change = True
			MapRender.shiftVboIndex(layer, posX, posY, -1)

	@staticmethod
	def shiftVboIndex(layer, posX, posY, indent=1):
		posY = MapRender.tHeight - posY - 1
		for x in range(posX, len(MapRender.tilesPosition[layer][posY])):
			if not MapRender.tilesPosition[layer][posY][x] == None:
				MapRender.tilesPosition[layer][posY][x] += indent

		for y in range(posY + 1, len(MapRender.tilesPosition[layer])):
			for x in range(len(MapRender.tilesPosition[layer][y])):
				if not MapRender.tilesPosition[layer][y][x] == None:
					MapRender.tilesPosition[layer][y][x] += indent

		for floor in range(layer + 1, len(MapRender.tilesPosition)):
			for y in range(posY, len(MapRender.tilesPosition[floor])):
				for x in range(len(MapRender.tilesPosition[floor][y])):
					if not MapRender.tilesPosition[floor][y][x] == None:
						MapRender.tilesPosition[floor][y][x] += indent

	@staticmethod
	def reserveNextVbo(layer, posX, posy):
		posY = MapRender.tHeight - posy - 1
		for x in range(posX, len(MapRender.tilesPosition[layer][posY])):
			if not MapRender.tilesPosition[layer][posY][x] == None:
				vbo = MapRender.tilesPosition[layer][posY][x]
				MapRender.shiftVboIndex(layer, x, posy)
				return vbo

		for y in range(posY + 1, len(MapRender.tilesPosition[layer])):
			for x in range(len(MapRender.tilesPosition[layer][y])):
				if not MapRender.tilesPosition[layer][y][x] == None:
					vbo = MapRender.tilesPosition[layer][y][x]
					MapRender.shiftVboIndex(layer, x, y)
					return vbo

		for floor in range(layer + 1, len(MapRender.tilesPosition)):
			for y in range(posY, len(MapRender.tilesPosition[floor])):
				for x in range(len(MapRender.tilesPosition[floor][y])):
					if not MapRender.tilesPosition[floor][y][x] == None:
						vbo = MapRender.tilesPosition[floor][y][x]
						MapRender.shiftVboIndex(floor, x, y)
						return vbo

		MapRender.vboCount +=1
		return MapRender.vboCount


	@staticmethod
	def unload():
		MapRender.shapeDown.unload()
		MapRender.shapeUp.unload()
		MapRender.tileSetImage.unload()
