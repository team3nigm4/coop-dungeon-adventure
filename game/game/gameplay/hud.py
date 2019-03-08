import json

from game.render.texture import texture
from game.render.shape import shape
from game.util import matrix4f
from game.render.shader.shadermanager import ShaderManager as sm
from game.game.entityclass.entitymanager import EntityManager as em


class Hud:
	hudSetImage = None
	hudSet = None
	hudInfo = None

	shape = None

	vbo = []
	ebo = []

	PORTRAIT_1 = 0
	PORTRAIT_2 = 1
	ITEM_1 = 2
	ITEM_2 = 3
	HEARTHS_1 = 4
	HEARTHS_2 = 7

	model = matrix4f.Matrix4f(True)
	itemName = ["", ""]

	@staticmethod
	def init():
		path_hudSetImage = "/hud/hudset.png"
		path_hudSet = "game/resources/textures/hud/hudset.json"
		Hud.hudSet = json.load(open(path_hudSet))
		Hud.hudSetImage = texture.Texture(path_hudSetImage)
		Hud.hudSetImage.load()

		Hud.shape = shape.Shape("hud", True)
		Hud.shape.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		Hud.shape.setReading([3, 2])

		Hud.model = matrix4f.Matrix4f(True)
		Hud.model.matrix[3][0] -= 9
		Hud.model.matrix[3][1] -= 6
		sm.updateLink("hud", "model", Hud.model.matrix)

		Hud.ebo = []
		for index in range(10):
			Hud.ebo.append(index * 4)
			Hud.ebo.append(index * 4 + 1)
			Hud.ebo.append(index * 4 + 3)
			Hud.ebo.append(index * 4 + 1)
			Hud.ebo.append(index * 4 + 2)
			Hud.ebo.append(index * 4 + 3)
		Hud.shape.setEbo(Hud.ebo)

		Hud.loadCharacteristiques()
		Hud.constructHud()

	@staticmethod
	def loadCharacteristiques():
		path_hudInfo = "game/resources/textures/hud/hudcharacteristics.json"
		Hud.hudInfo = json.load(open(path_hudInfo))

	@staticmethod
	def constructHud():
		Hud.vbo = [0 for a in range(20*10)]
		Hud.itemName1 = ""
		Hud.itemName2 = ""

		Hud.initElement(Hud.hudInfo["position"]["portrait1"],
						Hud.hudInfo["size"]["portrait1"], "portrait1", Hud.PORTRAIT_1)

		Hud.initElement(Hud.hudInfo["position"]["portrait2"],
						Hud.hudInfo["size"]["portrait2"], "portrait2", Hud.PORTRAIT_2)
		Hud.dispose()
		print("Hud len", len(Hud.vbo)/20)
		print(Hud.vbo)
		Hud.shape.setVbo(Hud.vbo)

	@staticmethod
	def display():
		sm.updateLink("hud", "model", Hud.model.matrix)
		Hud.hudSetImage.bind()
		Hud.shape.bind()
		Hud.shape.draw()

	@staticmethod
	def dispose():
		for i in range(1, 3):
			itemName = em.entities[i-1].getItemName()
			if not itemName[i-1] == itemName:
				if itemName == "Key":
					itemType = "item-key"
				elif itemName == "Weapon":
					if em.entities[i-1].item.arm:
						itemType = "item-sword"
					else:
						itemType = "item-bow"
				else:
					itemType = "item"

				Hud.initElement(Hud.hudInfo["position"]["item" + str(i)],
								Hud.hudInfo["size"]["item" + str(i)], itemType, 1+i)

	@staticmethod
	def initElement(position, size, texture, vboCount):
		del Hud.vbo[vboCount*20:(vboCount+1)*20]

		pos = Hud.hudSet["position"][texture]
		Hud.addVertice(position[0] - size[0]/2, position[1] - size[1]/2,
					pos[0], pos[1] + 1, vboCount)

		Hud.addVertice(position[0] + size[0]/2, position[1] - size[1]/2,
					pos[0] + 1, pos[1] + 1, vboCount)

		Hud.addVertice(position[0] + size[0]/2, position[1] + size[1]/2,
					pos[0] + 1, pos[1], vboCount)

		Hud.addVertice(position[0]- size[0]/2, position[1] + size[1]/2,
					pos[0], pos[1], vboCount)

	@staticmethod
	def addVertice(posX, posY, tposX, tposY, vboPos):
		vboPos *= 20
		posY += 1
		Hud.vbo.insert(vboPos, float(posX))
		Hud.vbo.insert(vboPos + 1, float(posY))
		Hud.vbo.insert(vboPos + 2, 0.0)
		Hud.vbo.insert(vboPos + 3, round(tposX / Hud.hudSet["info"]["size"][0], 3))
		Hud.vbo.insert(vboPos + 4,
							 Hud.hudSet["info"]["size"][1] - round(tposY / Hud.hudSet["info"]["size"][1], 3))
	@staticmethod
	def unload():
		Hud.hudSetImage.unload()
