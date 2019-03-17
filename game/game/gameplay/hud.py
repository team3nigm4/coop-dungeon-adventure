import json

from game.render.texture import texture
from game.render.shape import shape
from game.util import matrix4f
from game.render.shader.shadermanager import ShaderManager as sm
from game.game.entityclass import entitymanager as em


class Hud:
	PORTRAIT_1 = 0
	PORTRAIT_2 = 1
	ITEM_1 = 2
	ITEM_2 = 3
	HEARTHS_1 = 4
	HEARTHS_2 = 7

	VERTEX_SIZE = 4 * 6

	hudSetImage = None
	hudSet = None
	hudInfo = None

	shape = None

	vbo = []
	ebo = []

	model = matrix4f.Matrix4f(True)
	itemName = ["", ""]
	playerLife = [0, 0]
	playerInvincibility = [False, False]

	@staticmethod
	def init():
		path_hudSetImage = "hud/hudset.png"
		path_hudSet = "game/resources/textures/hud/hudset.json"
		Hud.hudSet = json.load(open(path_hudSet))
		Hud.hudSetImage = texture.Texture(path_hudSetImage)
		Hud.hudSetImage.load()

		Hud.shape = shape.Shape("hud", True)
		Hud.shape.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		Hud.shape.setReading([3, 2, 1])

		Hud.model = matrix4f.Matrix4f(True)
		Hud.model.matrix[3][0] -= 9
		Hud.model.matrix[3][1] -= 6

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
		Hud.vbo = [0 for a in range(Hud.VERTEX_SIZE * 10)]
		Hud.itemName1 = ""
		Hud.itemName2 = ""

		Hud.initElement(Hud.hudInfo["position"]["portrait1"],
						Hud.hudInfo["size"]["portrait1"], "portrait1",
						Hud.PORTRAIT_1, Hud.hudInfo["opacity"]["portrait1"])

		Hud.initElement(Hud.hudInfo["position"]["portrait2"],
						Hud.hudInfo["size"]["portrait2"], "portrait2",
						Hud.PORTRAIT_2, Hud.hudInfo["opacity"]["portrait2"])
		Hud.dispose()

	@staticmethod
	def display():
		sm.updateLink("hud", "model", Hud.model.matrix)
		
		Hud.hudSetImage.bind()
		Hud.shape.display()

	@staticmethod
	def dispose():
		ent = em.EntityManager
		change = False
		for i in range(2):
			itemName = ent.entities[i].getItemName()
			# If the item of the player change
			if not itemName[i] == itemName:
				if itemName == "Key":
					itemType = "item-key"
				elif itemName == "Weapon":
					if ent.entities[i].item.arm:
						itemType = "item-sword"
					else:
						itemType = "item-bow"
				else:
					itemType = "item"

				Hud.initElement(Hud.hudInfo["position"]["item" + str(i + 1)],
								Hud.hudInfo["size"]["item" + str(i + 1)],
								itemType, 2 + i, Hud.hudInfo["opacity"]["item" + str(i + 1)])
				change = True

			if not ent.entities[i].life == Hud.playerLife[i]:
				if ent.entities[i].takeDamage == Hud.playerInvincibility[i]:
					Hud.playerInvincibility[i] = not ent.entities[i].takeDamage
				Hud.setHealthBar(ent.entities[i].life, i)
				change = True

			elif ent.entities[i].takeDamage == Hud.playerInvincibility[i]:
				Hud.playerInvincibility[i] = not ent.entities[i].takeDamage
				Hud.setHealthBar(Hud.playerLife[i], i)
				change = True

		if change:
			Hud.shape.setVbo(Hud.vbo)

	@staticmethod
	def setHealthBar(newLife, i):
		Hud.playerLife[i] = newLife
		for a in range(3):
			if Hud.playerLife[i] >= a * 2 + 2:
				texture = "full-heart"
			elif Hud.playerLife[i] >= a * 2 + 1:
				texture = "half-heart"
			else:
				texture = "dead-heart"

			if Hud.playerInvincibility[i]:
				texture += "-save"

			position = Hud.hudInfo["position"]["healthBar" + str(i + 1)].copy()
			position[0] += (Hud.hudInfo["info"]["hearthGap"] * a)  + (Hud.hudInfo["size"]["hearth"][0] * a)

			if i == 0:
				Hud.initElement(position, Hud.hudInfo["size"]["hearth"],
								texture, Hud.HEARTHS_1 + a, Hud.hudInfo["opacity"]["healthBar1"])
			else:
				Hud.initElement(position, Hud.hudInfo["size"]["hearth"],
								texture, Hud.HEARTHS_2 + a, Hud.hudInfo["opacity"]["healthBar2"])

	@staticmethod
	def initElement(position, size, texture, vboCount, opacity):
		del Hud.vbo[vboCount * Hud.VERTEX_SIZE: (vboCount + 1) * Hud.VERTEX_SIZE]

		pos = Hud.hudSet["position"][texture]

		Hud.addVertice(position[0] - size[0] / 2, position[1] - size[1] / 2,
					pos[0], pos[1] + 1, vboCount, opacity)

		Hud.addVertice(position[0] + size[0] / 2, position[1] - size[1] / 2,
					pos[0] + 1, pos[1] + 1, vboCount, opacity)

		Hud.addVertice(position[0] + size[0] / 2, position[1] + size[1] / 2,
					pos[0] + 1, pos[1], vboCount, opacity)

		Hud.addVertice(position[0]- size[0]/2, position[1] + size[1]/2,
					pos[0], pos[1], vboCount, opacity)

	@staticmethod
	def addVertice(posX, posY, tposX, tposY, vboPos, opacity):
		vboPos *= Hud.VERTEX_SIZE
		posY += 1
		Hud.vbo.insert(vboPos, float(posX))
		Hud.vbo.insert(vboPos + 1, float(posY))
		Hud.vbo.insert(vboPos + 2, 0.0)
		Hud.vbo.insert(vboPos + 3, round(tposX / Hud.hudSet["info"]["size"][0], 3))
		Hud.vbo.insert(vboPos + 4,
							 Hud.hudSet["info"]["size"][1] - round(tposY / Hud.hudSet["info"]["size"][1], 3))
		Hud.vbo.insert(vboPos + 5, opacity)

	@staticmethod
	def unload():
		Hud.hudSetImage.unload()
