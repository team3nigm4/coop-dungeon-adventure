import json

from game.render.shape import shape
from game.render.texture import texture
from game.util import matrix4f
from game.render.shader.shadermanager import ShaderManager as sm
from game.game.entityclass import entitymanager as em


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
	transitionImage = None
	transitionPos = matrix4f.Matrix4f()
	transitionShape = None

	tWidth = 0
	tHeight = 0

	shapeUp = None
	shapeDown = None

	mapValues = [[]]
	tilesPosition = [[]]

	vbo = [[],[]]
	vboCount = [0, 0]
	ebo = [[],[]]
	eboCount = [0, 0]
	model = matrix4f.Matrix4f()

	change = [False, False]

	@staticmethod
	def init():
		# Images and json loading
		path_tileSetImage = "/tiles/tileset.png"
		path_tileSet = "game/resources/textures/tiles/tileset.json"
		path_transitionImage = "/hud/transition.png"

		MapRender.tileSet = json.load(open(path_tileSet))

		MapRender.tileSetImage = texture.Texture(path_tileSetImage)
		MapRender.tileSetImage.load()
		MapRender.transitionImage = texture.Texture(path_transitionImage)
		MapRender.transitionImage.load()

		MapRender.tileSize = MapRender.tileSet["info"]["tilesize"]
		MapRender.tileSet["info"]["size"] = [int(MapRender.tileSetImage.width/MapRender.tileSize), int(MapRender.tileSetImage.height/MapRender.tileSize)]
		MapRender.tileSet["id"] = []
		for y in range(0, int(MapRender.tileSetImage.height/MapRender.tileSize)):
			for x in range(0, int(MapRender.tileSetImage.width/MapRender.tileSize)):
				MapRender.tileSet["id"].append([x, y])

		# Render's shapes loading
		MapRender.shapeUp = shape.Shape("texture", True)
		MapRender.shapeUp.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		MapRender.shapeUp.setReading([3, 2])
		MapRender.shapeDown = shape.Shape("texture", True)
		MapRender.shapeDown.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		MapRender.shapeDown.setReading([3, 2])

		MapRender.model= matrix4f.Matrix4f(True)
		sm.updateLink("texture", "model", MapRender.model.matrix)

		from game.render.shape import entityrenderer as er
		MapRender.transitionShape = er.EntityRenderer()
		MapRender.transitionShape.setImagePath([18, 12], path_transitionImage, [0,0])

		# MapRender.transitionPos = matrix4f.Matrix4f(True)
		# MapRender.transitionShape = shape.Shape("hud", True)
		# MapRender.transitionShape.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		# quad = [0, 0, 0.0, 			0.0, 0.0, 	1.0,
		# 		18.0, 0, 0.0, 		1.0, 0.0, 	1.0,
		# 		18.0, 12.0, 0.0, 	1.0, 1.0, 	1.0,
		# 		0, 12.0, 0.0, 		0.0, 1.0,  	1.0]
		# indices = [0, 1, 2,		2, 3, 0]
		# MapRender.transitionShape.setEbo(indices)
		# MapRender.transitionShape.setVbo(quad)
		# MapRender.transitionShape.setReading([3, 2, 1])
		# MapRender.transitionPos.matrix[3][0] = -9
		# MapRender.transitionPos.matrix[3][1] = -6

	@staticmethod
	def constructMap():
		height = len(MapRender.mapValues[0])
		width = len(MapRender.mapValues[0][0])
		MapRender.tWidth = width
		MapRender.tHeight = height

		MapRender.tilesPosition = [[[None for sx in range(width)] for y in range(height)] for z in range(8)]

		MapRender.vbo = [[],[]]
		MapRender.ebo = [[],[]]
		MapRender.eboCount = [0, 0]
		MapRender.vboCount = [0, 0]

		for floor in range(8):
			if floor < 3:
				stage = 0
			else:
				stage = 1

			for y in range(len(MapRender.mapValues[floor])):
				for x in range(len(MapRender.mapValues[floor][y])):
					id = MapRender.mapValues[floor][y][x]
					if id != 0:
						pos = MapRender.tileSet["id"][id - 1]
						MapRender.addTile2(MapRender.vboCount[stage], floor, stage, x, height - y - 1, pos[0], pos[1])
						MapRender.vboCount[stage] += 1

		MapRender.change = [True, True]

	@staticmethod
	def display(transition):
		sm.updateLink("texture", "model", MapRender.model.matrix)
		MapRender.tileSetImage.bind()
		MapRender.shapeDown.display()

		em.EntityManager.display()

		sm.updateLink("texture", "model", MapRender.model.matrix)
		MapRender.tileSetImage.bind()
		MapRender.shapeUp.display()
		# print(MapRender.transitionPos.matrix)
		# sm.updateLink("hud", "model", MapRender.transitionPos.matrix)
		# MapRender.transitionImage.bind()
		# MapRender.transitionShape.display()
		if transition:
			MapRender.transitionShape.display()

	@staticmethod
	def dispose():
		if MapRender.change[0]:
			MapRender.shapeDown.setEbo(MapRender.ebo[0])
			MapRender.shapeDown.setVbo(MapRender.vbo[0])
			MapRender.change[0] = False

		if MapRender.change[1]:
			MapRender.shapeUp.setEbo(MapRender.ebo[1])
			MapRender.shapeUp.setVbo(MapRender.vbo[1])

	@staticmethod
	def setTransitionPos(pos):
		MapRender.transitionShape.updateModel(pos)

	@staticmethod
	def addTile(floor, posX, posY, textName, rotate=1):
		if floor < 3:
			stage = 0
		else:
			stage = 1

		vboCount = MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX]
		if vboCount is None:
			vboCount = MapRender.reserveNextVbo(floor, posX, posY)
		else: 
			MapRender.deleteTile(floor, posX, posY)
			MapRender.shiftVboIndex(floor, posX, posY)

		pos = MapRender.tileSet["tiles"][textName]
		MapRender.addTile2(vboCount, floor, stage, posX, posY, pos[0], pos[1], rotate)
		MapRender.change[stage] = True

	@staticmethod
	def addTile2(vboCount, floor, stage, posX, posY, tposX, tposY, rotate=1):
		eboIndex = MapRender.eboCount[stage] * 4

		MapRender.ebo[stage].append(eboIndex)
		MapRender.ebo[stage].append(eboIndex + 1)
		MapRender.ebo[stage].append(eboIndex + 3)
		MapRender.ebo[stage].append(eboIndex + 1)
		MapRender.ebo[stage].append(eboIndex + 2)
		MapRender.ebo[stage].append(eboIndex + 3)

		MapRender.eboCount[stage] +=1

		MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX] = vboCount	

		if rotate == 0:
			MapRender.addPos(stage, posX, posY - 1,
							 tposX, tposY, vboCount)

			MapRender.addPos(stage, posX + 1, posY - 1,
							 tposX, tposY + 1, vboCount)

			MapRender.addPos(stage, posX + 1, posY,
							 tposX + 1, tposY + 1, vboCount)

			MapRender.addPos(stage, posX, posY,
							 tposX + 1, tposY, vboCount)
		elif rotate == 2:
			MapRender.addPos(stage, posX, posY - 1,
							 tposX + 1, tposY + 1, vboCount)

			MapRender.addPos(stage, posX + 1, posY - 1,
							 tposX + 1, tposY, vboCount)

			MapRender.addPos(stage, posX + 1, posY,
							 tposX, tposY, vboCount)

			MapRender.addPos(stage, posX, posY,
							 tposX, tposY + 1, vboCount)
		elif rotate == 1:
			MapRender.addPos(stage, posX, posY - 1,
							 tposX, tposY + 1, vboCount)

			MapRender.addPos(stage, posX + 1, posY - 1,
							 tposX + 1, tposY + 1, vboCount)

			MapRender.addPos(stage, posX + 1, posY,
							 tposX + 1, tposY, vboCount)

			MapRender.addPos(stage, posX, posY,
							 tposX, tposY, vboCount)
		elif rotate == 3:
			MapRender.addPos(stage, posX, posY - 1,
							 tposX + 1, tposY, vboCount)

			MapRender.addPos(stage, posX + 1, posY - 1,
							 tposX, tposY, vboCount)

			MapRender.addPos(stage, posX + 1, posY,
							 tposX, tposY + 1, vboCount)

			MapRender.addPos(stage, posX, posY,
							 tposX + 1, tposY + 1, vboCount)

	@staticmethod
	def addPos(stage, posX, posY, tposX, tposY, vboPos):
		vboPos *= 20
		posY += 1
		MapRender.vbo[stage].insert(vboPos, float(posX))
		MapRender.vbo[stage].insert(vboPos + 1, float(posY))
		MapRender.vbo[stage].insert(vboPos + 2, 0.0)
		MapRender.vbo[stage].insert(vboPos + 3, round(tposX / MapRender.tileSet["info"]["size"][0], 3))
		MapRender.vbo[stage].insert(vboPos + 4,
							 MapRender.tileSet["info"]["size"][1] - round(tposY / MapRender.tileSet["info"]["size"][1], 3))

	@staticmethod
	def deleteTile(floor, posX, posY):
		if floor < 3:
			stage = 0
		else:
			stage = 1

		vbo = MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX]
		if not vbo == None:
			MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX] = None
			for i in range(20):
				del MapRender.vbo[stage][vbo * 20]
			for i in range(6):
				del MapRender.ebo[stage][len(MapRender.ebo) - 1]
			MapRender.eboCount[stage] -=1

			MapRender.change[stage] = True
			MapRender.shiftVboIndex(floor, posX, posY, -1)

	@staticmethod
	def shiftVboIndex(layer, posX, posY, indent=1):
		if layer < 3:
			end = 4
		else:
			end = 8

		posY = MapRender.tHeight - posY - 1
		for x in range(posX, len(MapRender.tilesPosition[layer][posY])):
			if not MapRender.tilesPosition[layer][posY][x] == None:
				MapRender.tilesPosition[layer][posY][x] += indent

		for y in range(posY + 1, len(MapRender.tilesPosition[layer])):
			for x in range(len(MapRender.tilesPosition[layer][y])):
				if not MapRender.tilesPosition[layer][y][x] == None:
					MapRender.tilesPosition[layer][y][x] += indent

		for floor in range(layer + 1, end):
			for y in range(posY, len(MapRender.tilesPosition[floor])):
				for x in range(len(MapRender.tilesPosition[floor][y])):
					if not MapRender.tilesPosition[floor][y][x] == None:
						MapRender.tilesPosition[floor][y][x] += indent

	@staticmethod
	def setMapValues(vbo, ebo, mapValue, tilesPositon, vboCount, eboCount):
		MapRender.mapValues = mapValue
		MapRender.tilesPosition = tilesPositon
		MapRender.vbo = vbo
		MapRender.ebo = ebo
		MapRender.vboCount  = vboCount
		MapRender.eboCount = eboCount

		MapRender.tWidth = len(MapRender.mapValues[0][0])
		MapRender.tHeight = len(MapRender.mapValues[0])
		width = MapRender.tWidth
		height = MapRender.tHeight

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
		MapRender.change = [True, True]
		MapRender.dispose()

	@staticmethod
	def reserveNextVbo(layer, posX, posy):
		if layer < 3:
			end = 4
		else:
			end = 8

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

		for floor in range(layer + 1, end):
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
		MapRender.transitionShape.unload()
		MapRender.transitionImage.unload()
