import json

from game.render.shape import shape
from game.util import matrix4f
from game.render.shader.shadermanager import ShaderManager as sm
from game.game.entityclass import entitymanager as em
from game.render.texture.texturemanager import TextureManager as tm


class MapRender:
	GROUND = 0
	GROUND2 = 1
	BASE_WALL = 2
	BASE_WALL2 = 3
	HIGH_WALL = 4
	HIGH_WALL2 = 5
	SUPP = 6
	SUPP2 = 7

	tileSets = {}
	currentTileSet = "tuto"

	transitionImage = None
	transitionPos = matrix4f.Matrix4f()
	transitionShape = None

	tWidth = 0
	tHeight = 0

	shapeUp = None
	shapeDown = None

	mapValues = [[[]]]
	tilesPosition = [[[]]]

	vbo = [[], []]
	vboCount = [0, 0]
	ebo = [[], []]
	eboCount = [0, 0]
	model = matrix4f.Matrix4f()

	change = [False, False]

	### Methods ###

	@staticmethod
	def addPos(stage, posX, posY, tposX, tposY, vboPos):
		vboPos *= 20
		posY += 1
		MapRender.vbo[stage].insert(vboPos, float(posX))
		MapRender.vbo[stage].insert(vboPos + 1, float(posY))
		MapRender.vbo[stage].insert(vboPos + 2, 0.0)
		MapRender.vbo[stage].insert(vboPos + 3,
									round(tposX / MapRender.tileSets[MapRender.currentTileSet]["info"]["size"][0], 4))
		MapRender.vbo[stage].insert(vboPos + 4,
									MapRender.tileSets[MapRender.currentTileSet]["info"]["size"][1] -
									round(tposY / MapRender.tileSets[MapRender.currentTileSet]["info"]["size"][1], 4))

	@staticmethod
	def addTile(floor, posX, posY, textName, rotate=1):
		texPos = MapRender.tileSets[MapRender.currentTileSet]["decor"][textName]["pos"]
		MapRender.addTileTexPos(floor, posX, posY, texPos[0], texPos[1], rotate)

	@staticmethod
	def addTileTexPos(floor, posX, posY, texPosX, texPosY, rotate=1):
		if posX < 0 or posX >= len(MapRender.mapValues[0][0]):
			return

		if posY < 0 or posY >= len(MapRender.mapValues[0]):
			return
		if floor <= 3:
			stage = 0
		else:
			stage = 1

		vboCount = MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX]
		if vboCount == None:
			vboCount = MapRender.reserveNextVbo(floor, posX, posY)
		else:
			MapRender.deleteTile(floor, posX, posY)
			MapRender.shiftVboIndex(floor, posX, posY)

		MapRender.addTile2(vboCount, floor, stage, posX, posY, texPosX, texPosY, rotate)
		MapRender.change[stage] = True

	@staticmethod
	def addTile2(vboCount, floor, stage, posX, posY, tposX, tposY, rotate=1):
		if posX < 0 or posX >= len(MapRender.mapValues[0][0]):
			return

		if posY < 0 or posY >= len(MapRender.mapValues[0]):
			return

		eboIndex = MapRender.eboCount[stage] * 4

		MapRender.ebo[stage].append(eboIndex)
		MapRender.ebo[stage].append(eboIndex + 1)
		MapRender.ebo[stage].append(eboIndex + 3)
		MapRender.ebo[stage].append(eboIndex + 1)
		MapRender.ebo[stage].append(eboIndex + 2)
		MapRender.ebo[stage].append(eboIndex + 3)

		MapRender.eboCount[stage] += 1

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
	def addDecor(decor, posX, posY):
		if decor == "delete" or decor == "null":
			return

		layer = MapRender.tileSets[MapRender.currentTileSet]["decor"][decor]["layer"]

		texPos = MapRender.tileSets[MapRender.currentTileSet]["decor"][decor]["pos"]
		for y in range(MapRender.tileSets[MapRender.currentTileSet]["decor"][decor]["size"][1] - 1, -1, -1):
			for x in range(MapRender.tileSets[MapRender.currentTileSet]["decor"][decor]["size"][0]):
				MapRender.addTileTexPos(layer, posX + x, posY + y, texPos[0] + x, texPos[1] - y)

	@staticmethod
	def deleteDecor(oldDecor, posX, posY):
		if oldDecor == "delete" or oldDecor == "null":
			return

		layer = MapRender.tileSets[MapRender.currentTileSet]["decor"][oldDecor]["layer"]
		for y in range(MapRender.tileSets[MapRender.currentTileSet]["decor"][oldDecor]["size"][1]):
			for x in range(MapRender.tileSets[MapRender.currentTileSet]["decor"][oldDecor]["size"][0] -1, -1, -1):
				MapRender.deleteTile(layer, posX + x, posY + y)

	@staticmethod
	def constructMap():
		height = len(MapRender.mapValues[0])
		width = len(MapRender.mapValues[0][0])
		MapRender.tWidth = width
		MapRender.tHeight = height

		MapRender.tilesPosition = [[[None for x in range(width)] for y in range(height)] for z in range(8)]

		MapRender.vbo = [[], []]
		MapRender.ebo = [[], []]
		MapRender.eboCount = [0, 0]
		MapRender.vboCount = [0, 0]

		for floor in range(8):
			if floor <= 3:
				stage = 0
			else:
				stage = 1

			for y in range(len(MapRender.mapValues[floor])):
				for x in range(len(MapRender.mapValues[floor][y])):
					id = MapRender.mapValues[floor][y][x]
					if id != 0:
						pos = MapRender.tileSets[MapRender.currentTileSet]["id"][id - 1]
						MapRender.addTile2(MapRender.vboCount[stage], floor, stage, x, height - y - 1, pos[0], pos[1])
						MapRender.vboCount[stage] += 1

		MapRender.change = [True, True]

	@staticmethod
	def deleteTile(floor, posX, posY):
		if posX < 0 or posX >= len(MapRender.mapValues[0][0]):
			return

		if posY < 0 or posY >= len(MapRender.mapValues[0]):
			return

		if floor <= 3:
			stage = 0
		else:
			stage = 1

		vbo = MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX]

		if vbo == None:
			return
		else:
			MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX] = None
			size = len(MapRender.ebo[stage])
			for i in range(6):
				del MapRender.ebo[stage][size - 1 - i]

			for i in range(20):
				del MapRender.vbo[stage][vbo * 20 - i - 1]
			MapRender.vboCount[stage] -=1
			MapRender.eboCount[stage] -= 1

			MapRender.change[stage] = True
			MapRender.shiftVboIndex(floor, posX, posY, -1)

	@staticmethod
	def display(transition):
		sm.updateLink("texture", "model", MapRender.model.matrix)
		tm.bind(MapRender.currentTileSet)
		MapRender.shapeDown.display()

		em.EntityManager.display()

		sm.updateLink("texture", "model", MapRender.model.matrix)
		tm.bind(MapRender.currentTileSet)
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
	def init():
		# Images and json loading
		MapRender.loadTileSets()

		# Render's shapes loading
		MapRender.shapeUp = shape.Shape("texture", True)
		MapRender.shapeUp.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		MapRender.shapeUp.setReading([3, 2])
		MapRender.shapeDown = shape.Shape("texture", True)
		MapRender.shapeDown.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		MapRender.shapeDown.setReading([3, 2])

		MapRender.model = matrix4f.Matrix4f(True)
		sm.updateLink("texture", "model", MapRender.model.matrix)

		from game.render.shape import entityrenderer as er
		MapRender.transitionShape = er.EntityRenderer()
		MapRender.transitionShape.setImage([18, 12], "transition", [0, 0])

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
	def loadTileSets():
		# List of tileSet
		list = json.load(open("game/resources/textures/tiles/list.json")).copy()
		list = list["tileSets"]

		# Load json tileSet files
		for tileSet in list:
			curTileSet = tm.textures[tileSet]
			MapRender.tileSets.update({tileSet: json.load(open("game/resources/textures/tiles/" + tileSet + ".json"))})
			MapRender.tileSize = MapRender.tileSets[tileSet]["info"]["tilesize"]
			MapRender.tileSets[tileSet]["info"]["size"] = [
				int(curTileSet.width / MapRender.tileSize),
				int(curTileSet.height / MapRender.tileSize)]
			MapRender.tileSets[tileSet]["id"] = []
			for y in range(0, int(curTileSet.height / MapRender.tileSize)):
				for x in range(0, int(curTileSet.width / MapRender.tileSize)):
					MapRender.tileSets[tileSet]["id"].append([x, y])

	@staticmethod
	def reserveNextVbo(layer, posX, posY):
		if layer <= 3:
			end = 4
			stage = 0
		else:
			end = 8
			stage = 1

		posY = MapRender.tHeight - posY - 1
		for x in range(posX, len(MapRender.tilesPosition[layer][posY])):
			if not MapRender.tilesPosition[layer][posY][x] == None:
				vbo = MapRender.tilesPosition[layer][posY][x]
				MapRender.shiftVboIndex(layer, x, posY)
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

		MapRender.vboCount[stage] += 1
		return MapRender.vboCount[stage]

	@staticmethod
	def setMapValues(vbo, ebo, mapValue, tilesPositon, vboCount, eboCount, tileSet):
		MapRender.mapValues = mapValue
		MapRender.tilesPosition = tilesPositon
		MapRender.vbo = vbo
		MapRender.ebo = ebo
		MapRender.vboCount = vboCount
		MapRender.eboCount = eboCount
		MapRender.currentTileSet = tileSet

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
	def setTransitionPos(pos):
		MapRender.transitionShape.updateModel(pos)

	@staticmethod
	def shiftVboIndex(layer, posX, posY, indent=1):
		if layer <= 3:
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
	def unload():
		MapRender.shapeDown.unload()
		MapRender.shapeUp.unload()
		MapRender.transitionShape.unload()
