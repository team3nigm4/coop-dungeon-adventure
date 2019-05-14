# Static class to render the hud

import json

from game.render.texture.texturemanager import TextureManager as tm
from game.render.shape import shape
from game.util import matrix4f
from game.render.shader.shadermanager import ShaderManager as sm
from game.game.entityclass import entitymanager as em


class Hud:
	BACK_1 = 1
	BACK_2 = 2
	PORTRAIT_1 = 3
	PORTRAIT_2 = 4
	FRAME_ITEM_1 = 5
	FRAME_ITEM_2 = 6
	ITEM_1 = 7
	ITEM_2 = 8
	HEARTHS_1 = 9
	HEARTHS_2 = 12
	SWITCH_1 = 15
	SWITCH_2 = 16
	ITEM_SWITCH_1 = 17
	ITEM_SWITCH_2 = 18

	ELEMENT_TO_DRAW = 19

	VERTEX_SIZE = 4 * 6

	hudSetImage = None
	hudSet = None
	hudInfo = None

	shape = None

	vbo = []
	ebo = []

	model = matrix4f.Matrix4f(True)
	itemName = ["null", "null"]
	subItemName = ["null", "null"]
	playerLife = [0, 0]
	playerInvincibility = [False, False]
	playerInteraction = [False, False]

	@staticmethod
	def init():
		path_hudSet = "game/resources/textures/hud/hudset.json"
		Hud.hudSet = json.load(open(path_hudSet))

		Hud.shape = shape.Shape("texture-hud", True)
		Hud.shape.setStorage(shape.Shape.STATIC_STORE, shape.Shape.STATIC_STORE)
		Hud.shape.setReading([3, 2, 1])

		Hud.model = matrix4f.Matrix4f(True)
		Hud.model.matrix[3][0] -= 9
		Hud.model.matrix[3][1] -= 6

		Hud.ebo = []
		for index in range(Hud.ELEMENT_TO_DRAW):
			Hud.ebo.append(index * 4)
			Hud.ebo.append(index * 4 + 1)
			Hud.ebo.append(index * 4 + 3)
			Hud.ebo.append(index * 4 + 1)
			Hud.ebo.append(index * 4 + 2)
			Hud.ebo.append(index * 4 + 3)
		Hud.shape.setEbo(Hud.ebo)

		Hud.itemName = ["null", "null"]
		Hud.subItemName = ["null", "null"]
		Hud.playerLife = [0, 0]
		Hud.playerInvincibility = [False, False]
		Hud.playerInteraction = [False, False]

		Hud.loadCharacteristiques()
		Hud.constructHud()

	# Load characteristics because this document control positions and sizes of each element of hud
	@staticmethod
	def loadCharacteristiques():
		path_hudInfo = "game/resources/textures/hud/hudcharacteristics.json"
		Hud.hudInfo = json.load(open(path_hudInfo))

	# Construct the hud
	@staticmethod
	def constructHud():
		Hud.vbo = [0 for a in range(Hud.VERTEX_SIZE * Hud.ELEMENT_TO_DRAW)]
		Hud.itemName1 = ""
		Hud.itemName2 = ""

		Hud.constructElement(Hud.hudInfo["position"]["back-1"],
							 Hud.hudInfo["size"]["back-1"], "back",
							 Hud.BACK_1, Hud.hudInfo["opacity"]["back-1"])

		Hud.constructElement(Hud.hudInfo["position"]["back-2"],
							 Hud.hudInfo["size"]["back-2"], "back",
							 Hud.BACK_2, Hud.hudInfo["opacity"]["back-2"])

		Hud.constructElement(Hud.hudInfo["position"]["portrait-1"],
							 Hud.hudInfo["size"]["portrait-1"], "portrait-1",
							 Hud.PORTRAIT_1, Hud.hudInfo["opacity"]["portrait-1"])

		Hud.constructElement(Hud.hudInfo["position"]["portrait-2"],
							 Hud.hudInfo["size"]["portrait-2"], "portrait-2",
							 Hud.PORTRAIT_2, Hud.hudInfo["opacity"]["portrait-2"])

		Hud.constructElement(Hud.hudInfo["position"]["frame-item-1"],
							 Hud.hudInfo["size"]["frame-item-1"],
						"frame-item-1", Hud.FRAME_ITEM_1, Hud.hudInfo["opacity"]["frame-item-1"])

		Hud.constructElement(Hud.hudInfo["position"]["frame-item-2"],
							 Hud.hudInfo["size"]["frame-item-2"],
						"frame-item-2", Hud.FRAME_ITEM_2, Hud.hudInfo["opacity"]["frame-item-2"], True)

		Hud.dispose()

	@staticmethod
	def display():
		sm.updateLink("texture-hud", "model", Hud.model.matrix)

		tm.bind("hud")
		Hud.shape.display()

	# Check state game to change the hud
	@staticmethod
	def dispose():
		ent = em.EntityManager
		change = False


		itemName = [ent.entities[0].getItemName(), ent.entities[1].getItemName()]
		# For both players
		for i in range(2):
			# If players change their items
			hasChange = False
			if not Hud.itemName[0] == itemName[0] or not Hud.itemName[1] == itemName[1]:
				hasChange = True

			if itemName[i] == "Weapon":
				if not Hud.subItemName[i] == ent.entities[i].item.arm:
					hasChange = True

			if hasChange:
				if Hud.itemName[i] == "Weapon":
					Hud.constructElement([0, 0], [1, 1], "null", Hud.ITEM_SWITCH_1 + i, 0)

					Hud.constructElement([0, 0], [1, 1], "null", Hud.SWITCH_1 + i, 0)

				if itemName[i] == "Null":
					Hud.constructElement([0, 0], [1, 1], "null", Hud.ITEM_1 + i, 0)
				else:

					itemType = "item-key"
					switch = [False]

					if itemName[i] == "Key":
						itemType = "item-key"

					elif itemName[i] == "Weapon":
						if ent.entities[i].item.arm:
							itemType = "item-sword"
							Hud.subItemName[i] = itemType
							if not itemName[1 - i] == "Weapon":
								switch = [True, "item-bow"]
							else:
								switch = [False]
						else:
							itemType = "item-bow"
							Hud.subItemName[i] = itemType
							if not itemName[1 - i] == "Weapon":
								switch = [True, "item-sword"]
							else:
								switch = [False]

					if i == 0:
						flip = False
					else:
						flip = True

					# Display new Item

					Hud.constructElement(Hud.hudInfo["position"]["frame-item-" + str(i + 1)],
										 Hud.hudInfo["size"]["frame-item-" + str(i + 1)],
										 itemType, Hud.ITEM_1 + i, Hud.hudInfo["opacity"]["frame-item-" + str(i + 1)], flip)

					# Display switch state if item with switch
					if switch[0]:
						Hud.constructElement(Hud.hudInfo["position"]["switch-" + str(i + 1)],
											 Hud.hudInfo["size"]["switch"],
										"switch", Hud.SWITCH_1 + i, Hud.hudInfo["opacity"]["switch"], flip)

						Hud.constructElement(Hud.hudInfo["position"]["item-switch-" + str(i + 1)],
											 Hud.hudInfo["size"]["item-switch"],
											 switch[1], Hud.ITEM_SWITCH_1 + i, Hud.hudInfo["opacity"]["item-switch"], flip)

				change = True

			# If players life change
			if not ent.entities[i].life == Hud.playerLife[i]:
				if ent.entities[i].takeDamage == Hud.playerInvincibility[i]:
					Hud.playerInvincibility[i] = not ent.entities[i].takeDamage
				Hud.setHealthBar(ent.entities[i].life, i)
				change = True

			# If players invincibility change
			elif ent.entities[i].takeDamage == Hud.playerInvincibility[i]:
				Hud.playerInvincibility[i] = not ent.entities[i].takeDamage
				Hud.setHealthBar(Hud.playerLife[i], i)
				change = True

			# If players interaction change
			if not Hud.playerInteraction[i] == ent.entities[i].getCanInteract():
				change = True
				Hud.playerInteraction[i] = ent.entities[i].getCanInteract()
				if Hud.playerInteraction[i]:
					type = "portrait-interaction-"
				else:
					type = "portrait-"
				Hud.constructElement(Hud.hudInfo["position"]["portrait-" + str(i + 1)],
									 Hud.hudInfo["size"]["portrait-" +  str(i + 1)], type + str(i + 1),
									 Hud.PORTRAIT_1 + i, Hud.hudInfo["opacity"]["portrait-" +  str(i + 1)])

		# If there is a hud change, apply it
		if change:
			Hud.itemName[0] = itemName[0]
			Hud.itemName[1] = itemName[1]
			Hud.shape.setVbo(Hud.vbo)

	# Reconstruct the health bar
	@staticmethod
	def setHealthBar(newLife, i):
		Hud.playerLife[i] = newLife
		# For three hearth
		for a in range(3):
			if Hud.playerLife[i] >= a * 2 + 2:
				texture = "full-heart"
			elif Hud.playerLife[i] >= a * 2 + 1:
				texture = "half-heart"
			else:
				texture = "dead-heart"

			if Hud.playerInvincibility[i]:
				texture = "protect-heart"

			position = Hud.hudInfo["position"]["health-bar-" + str(i + 1)].copy()
			position[0] += (Hud.hudInfo["info"]["heart-gap"] * a)  + (Hud.hudInfo["size"]["hearth"][0] * a)

			if i == 0:
				Hud.constructElement(position, Hud.hudInfo["size"]["hearth"],
									 texture, Hud.HEARTHS_1 + a, Hud.hudInfo["opacity"]["health-bar-1"])
			else:
				Hud.constructElement(position, Hud.hudInfo["size"]["hearth"],
									 texture, Hud.HEARTHS_2 + a, Hud.hudInfo["opacity"]["health-bar-2"])

	# Construct an element of the hud using OpenGL functionality
	@staticmethod
	def constructElement(position, size, texture, vboCount, opacity, flip=False):
		del Hud.vbo[vboCount * Hud.VERTEX_SIZE: (vboCount + 1) * Hud.VERTEX_SIZE]

		if texture == "null":
			texPos = [0, 0]
			texSize = [0, 0]

		else:
			texPos = Hud.hudSet["elements"][texture]["pos"]

			if "size" in Hud.hudSet["elements"][texture]:
				texSize = Hud.hudSet["elements"][texture]["size"]
			else:
				texSize = [1, 1]

		# Flip some elements for the other play
		if flip:
			Hud.addVertice(position[0] + size[0] / 2, position[1] - size[1] / 2,
						   texPos[0], texPos[1] + texSize[1], vboCount, opacity)

			Hud.addVertice(position[0] - size[0] / 2, position[1] - size[1] / 2,
						   texPos[0] + texSize[0], texPos[1] + texSize[1], vboCount, opacity)

			Hud.addVertice(position[0] - size[0] / 2, position[1] + size[1] / 2,
						   texPos[0] + texSize[0], texPos[1], vboCount, opacity)

			Hud.addVertice(position[0] + size[0] / 2, position[1] + size[1] / 2,
						   texPos[0], texPos[1], vboCount, opacity)
		else:
			Hud.addVertice(position[0] - size[0] / 2, position[1] - size[1] / 2,
						   texPos[0], texPos[1] + texSize[1], vboCount, opacity)

			Hud.addVertice(position[0] + size[0] / 2, position[1] - size[1] / 2,
						   texPos[0] + texSize[0], texPos[1] + texSize[1], vboCount, opacity)

			Hud.addVertice(position[0] + size[0] / 2, position[1] + size[1] / 2,
						   texPos[0] + texSize[0], texPos[1], vboCount, opacity)

			Hud.addVertice(position[0] - size[0]/2, position[1] + size[1]/2,
						   texPos[0], texPos[1], vboCount, opacity)

	# 4 vertices for a square information of position, texture position and opacity
	@staticmethod
	def addVertice(posX, posY, tposX, tposY, vboPos, opacity):
		vboPos *= Hud.VERTEX_SIZE
		posY += 1
		Hud.vbo.insert(vboPos, float(posX))
		Hud.vbo.insert(vboPos + 1, float(posY))
		Hud.vbo.insert(vboPos + 2, 0.0)
		Hud.vbo.insert(vboPos + 3, round(tposX / Hud.hudSet["info"]["size"][0], 4))
		Hud.vbo.insert(vboPos + 4,
							 Hud.hudSet["info"]["size"][1] - round(tposY / Hud.hudSet["info"]["size"][1], 4))
		Hud.vbo.insert(vboPos + 5, opacity)

	@staticmethod
	def unload():
		Hud.shape.unload()
