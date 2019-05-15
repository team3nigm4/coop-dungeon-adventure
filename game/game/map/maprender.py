# Static class to render the map

import json

from game.render.shape import shape
from game.util import matrix4f
from game.render.shader.shadermanager import ShaderManager as sm
from game.game.entityclass import entitymanager as em
from game.render.texture.texturemanager import TextureManager as tm
from game.render.shape import guirenderer


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

	mapValues = [[[]]]
	# Position per tile in vbo (object to display)
	tilesPosition = [[[]]]

	# Two part off map are displayed
	# Layer 0 -> 3 and layer 4 -> 7 (entities are displayed between)
	shapeUp = None
	shapeDown = None
	vbo = [[], []]
	vboCount = [0, 0]
	ebo = [[], []]
	eboCount = [0, 0]
	model = matrix4f.Matrix4f()

	change = [False, False]

	### Methods ###

	# 4 vertices for a square with information of position, texture position on each vertix
	@staticmethod
	def addVertex(stage, posX, posY, tposX, tposY, vboPos):
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

	# Add a tile without knowing its place in the tile set
	@staticmethod
	def addTile(floor, posX, posY, textName, rotate=1):
		texPos = MapRender.tileSets[MapRender.currentTileSet]["decor"][textName]["pos"]
		MapRender.addTileTexPos(floor, posX, posY, texPos[0], texPos[1], rotate)

	# Add a tile knowing its place in the tile set
	@staticmethod
	def addTileTexPos(floor, posX, posY, texPosX, texPosY, rotate=1):
		if posX < 0 or posX >= len(MapRender.mapValues[0][0]):
			return

		if posY < 0 or posY >= len(MapRender.mapValues[0]):
			return

		# Choose the part
		if floor <= 3:
			stage = 0
		else:
			stage = 1

		# Take the vbo in this tile
		vboCount = MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX]

		# If the tile is free
		if vboCount == -1:
			vboCount = MapRender.reserveNextVbo(floor, posX, posY)
			MapRender.shiftVboIndex(floor, posX, posY)
		# If there is already a tile
		else:
			MapRender.deleteTile(floor, posX, posY)
			MapRender.shiftVboIndex(floor, posX, posY)

		# Create the tile to the position
		MapRender.addTile2(vboCount, floor, stage, posX, posY, texPosX, texPosY, rotate)
		MapRender.change[stage] = True

	@staticmethod
	def addTile2(vboCount, floor, stage, posX, posY, tposX, tposY, rotate=1):
		# Securities
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

		# Construct the tile differently depending on the rotation (base is 1)
		if rotate == 0:  # To left
			MapRender.addVertex(stage, posX, posY - 1,
							 tposX, tposY, vboCount)

			MapRender.addVertex(stage, posX + 1, posY - 1,
								tposX, tposY + 1, vboCount)

			MapRender.addVertex(stage, posX + 1, posY,
								tposX + 1, tposY + 1, vboCount)

			MapRender.addVertex(stage, posX, posY,
								tposX + 1, tposY, vboCount)
		elif rotate == 2:  # To right
			MapRender.addVertex(stage, posX, posY - 1,
							 tposX + 1, tposY + 1, vboCount)

			MapRender.addVertex(stage, posX + 1, posY - 1,
								tposX + 1, tposY, vboCount)

			MapRender.addVertex(stage, posX + 1, posY,
								tposX, tposY, vboCount)

			MapRender.addVertex(stage, posX, posY,
								tposX, tposY + 1, vboCount)
		elif rotate == 1:  # To up (normal)
			MapRender.addVertex(stage, posX, posY - 1,
							 tposX, tposY + 1, vboCount)

			MapRender.addVertex(stage, posX + 1, posY - 1,
								tposX + 1, tposY + 1, vboCount)

			MapRender.addVertex(stage, posX + 1, posY,
								tposX + 1, tposY, vboCount)

			MapRender.addVertex(stage, posX, posY,
								tposX, tposY, vboCount)
		elif rotate == 3:  # To down
			MapRender.addVertex(stage, posX, posY - 1,
							 tposX + 1, tposY, vboCount)

			MapRender.addVertex(stage, posX + 1, posY - 1,
								tposX, tposY, vboCount)

			MapRender.addVertex(stage, posX + 1, posY,
								tposX, tposY + 1, vboCount)

			MapRender.addVertex(stage, posX, posY,
								tposX + 1, tposY + 1, vboCount)

	# Add a decor with its name
	@staticmethod
	def addDecor(decor, posX, posY):
		# Securities
		if decor == "delete" or decor == "null":
			return

		layer = MapRender.tileSets[MapRender.currentTileSet]["decor"][decor]["layer"]

		# Position of the decor in the tile set
		texPos = MapRender.tileSets[MapRender.currentTileSet]["decor"][decor]["pos"]

		# Add the decor left to right and top to bottom
		for y in range(MapRender.tileSets[MapRender.currentTileSet]["decor"][decor]["size"][1] - 1, -1, -1):
			for x in range(MapRender.tileSets[MapRender.currentTileSet]["decor"][decor]["size"][0]):
				MapRender.addTileTexPos(layer, posX + x, posY + y, texPos[0] + x, texPos[1] - y)

	# Delete a decor with its name
	@staticmethod
	def deleteDecor(oldDecor, posX, posY):
		# Securities
		if oldDecor == "delete" or oldDecor == "null":
			return

		layer = MapRender.tileSets[MapRender.currentTileSet]["decor"][oldDecor]["layer"]

		# Delete the decor right to left and bottom to up
		for y in range(MapRender.tileSets[MapRender.currentTileSet]["decor"][oldDecor]["size"][1]):
			for x in range(MapRender.tileSets[MapRender.currentTileSet]["decor"][oldDecor]["size"][0] -1, -1, -1):
				MapRender.deleteTile(layer, posX + x, posY + y)

	# First method called for the first map construction, this construct is based on map json table
	@staticmethod
	def constructMap():
		height = len(MapRender.mapValues[0])
		width = len(MapRender.mapValues[0][0])
		MapRender.tWidth = width
		MapRender.tHeight = height

		# Set values
		MapRender.tilesPosition = [[[-1 for x in range(width)] for y in range(height)] for z in range(8)]
		MapRender.vbo = [[], []]
		MapRender.ebo = [[], []]
		MapRender.eboCount = [0, 0]
		MapRender.vboCount = [0, 0]

		# 7 layers
		for floor in range(8):
			# Choose the part
			if floor <= 3:
				stage = 0
			else:
				stage = 1

			for y in range(len(MapRender.mapValues[floor])):
				for x in range(len(MapRender.mapValues[floor][y])):
					# With the id, fill a tile with position in vbo
					id = MapRender.mapValues[floor][y][x]
					if id != 0:
						pos = MapRender.tileSets[MapRender.currentTileSet]["id"][id - 1]
						MapRender.addTile2(MapRender.vboCount[stage], floor, stage, x, height - y - 1, pos[0], pos[1])
						MapRender.vboCount[stage] += 1

		MapRender.change = [True, True]

	@staticmethod
	def deleteTile(floor, posX, posY):
		# Securities
		if posX < 0 or posX >= len(MapRender.mapValues[0][0]):
			return

		if posY < 0 or posY >= len(MapRender.mapValues[0]):
			return

		# Choose the part
		if floor <= 3:
			stage = 0
		else:
			stage = 1

		vbo = MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX]

		# Can't delete a not existing tile
		if vbo == -1:
			return
		else:
			MapRender.tilesPosition[floor][MapRender.tHeight - posY - 1][posX] = -1
			size = len(MapRender.ebo[stage])
			for i in range(6):
				del MapRender.ebo[stage][size - 1 - i]

			for i in range(20):
				del MapRender.vbo[stage][vbo * 20]
			MapRender.vboCount[stage] -= 1
			MapRender.eboCount[stage] -= 1

			MapRender.change[stage] = True
			MapRender.shiftVboIndex(floor, posX, posY, -1)

	@staticmethod
	def display(transition):
		# Displays two parts for maps:
		# Displays fist layer 0 -> 3, then answers EntityManager to display entities and finally display layer 4 -> 7

		sm.updateLink("texture", "model", MapRender.model.matrix)
		tm.bind(MapRender.currentTileSet)
		MapRender.shapeDown.display()

		em.EntityManager.display()

		sm.updateLink("texture", "model", MapRender.model.matrix)
		tm.bind(MapRender.currentTileSet)
		MapRender.shapeUp.display()
		if transition:
			MapRender.transitionShape.display()

	@staticmethod
	def dispose():
		# Reapply values for shape with the new version of vbo and ebo

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

		MapRender.transitionShape = guirenderer.GuiRenderer()
		MapRender.transitionShape.setImage([18, 12], "transition")
		MapRender.transitionShape.updateModel([9, 6])

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
		# Choose the part
		if layer <= 3:
			end = 4
			stage = 0
		else:
			end = 8
			stage = 1

		# Invert position of posY
		posY = MapRender.tHeight - posY - 1

		posX += 1
		# Check next tiles in the same row
		for x in range(posX, len(MapRender.tilesPosition[layer][posY])):
			if not MapRender.tilesPosition[layer][posY][x] == -1:
				vbo = MapRender.tilesPosition[layer][posY][x]
				return vbo

		# Check next tiles in the same layer
		for y in range(posY + 1, len(MapRender.tilesPosition[layer])):
			for x in range(len(MapRender.tilesPosition[layer][y])):
				if not MapRender.tilesPosition[layer][y][x] == -1:
					vbo = MapRender.tilesPosition[layer][y][x]
					return vbo

		# Check next tiles after its layer
		for floor in range(layer + 1, end):
			for y in range(len(MapRender.tilesPosition[floor])):
				for x in range(len(MapRender.tilesPosition[floor][y])):
					if not MapRender.tilesPosition[floor][y][x] == -1:
						vbo = MapRender.tilesPosition[floor][y][x]
						return vbo

		vbo = MapRender.vboCount[stage]
		MapRender.vboCount[stage] += 1
		return vbo

	# MapTemporarySave send values to apply during the map changing
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

		# Set camera position according to the size of map
		# In x
		if width > 18:
			# Follow the player
			cam.track[0] = True
		else:
			# Don't move
			cam.track[0] = False
			cam.addPos([-width / 2, 0, 0])
		# In y
		if height > 12:
			# Follow the player
			cam.track[1] = True
		else:
			# Don't move
			cam.track[1] = False
			cam.addVertex([0, -height / 2, 0])

		cam.goToEntity()
		sm.dispose()
		MapRender.change = [True, True]
		MapRender.dispose()

	@staticmethod
	def setTransitionPos(pos):
		MapRender.transitionShape.updateModel(pos)

	# Add a value (indent) for every tiles after one
	@staticmethod
	def shiftVboIndex(layer, posX, posY, indent=1):
		# Choose the part
		if layer <= 3:
			end = 4
		else:
			end = 8

		# Invert position of posY
		posY = MapRender.tHeight - posY - 1

		posX += 1

		# Check next tile in the same row
		for x in range(posX, len(MapRender.tilesPosition[layer][posY])):
			if not MapRender.tilesPosition[layer][posY][x] == -1:
				MapRender.tilesPosition[layer][posY][x] += indent

		# Check next tile in the same layer
		for y in range(posY + 1, len(MapRender.tilesPosition[layer])):
			for x in range(len(MapRender.tilesPosition[layer][y])):
				if not MapRender.tilesPosition[layer][y][x] == -1:
					MapRender.tilesPosition[layer][y][x] += indent

		# Check next tile after its layer
		for floor in range(layer + 1, end):
			for y in range(len(MapRender.tilesPosition[floor])):
				for x in range(len(MapRender.tilesPosition[floor][y])):
					if not MapRender.tilesPosition[floor][y][x] == -1:
						MapRender.tilesPosition[floor][y][x] += indent

	@staticmethod
	def unload():
		MapRender.shapeDown.unload()
		MapRender.shapeUp.unload()
		MapRender.transitionShape.unload()

		del MapRender.shapeDown
		del MapRender.shapeUp
		del MapRender.transitionShape
