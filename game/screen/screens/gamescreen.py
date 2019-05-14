# Class to update/display the game 

from game.game.entitymodel import player as 						pl
from game.game.entityclass.entitymanager import EntityManager as 	em
from game.game.map.mapmanager import MapManager as 					mam
from game.inputs.inputmanager import InputManager as 				im
from game.inputs.keyboardmanager import KeyBoardManager as 			kbm
from game.screen.gamemanager import GameManager as 					gm
from game.screen.screens import screen
from game.game.gameplay.hud import Hud
from game.render.text import text
from game.render.shape import guirenderer
from game.render.gui import button
from game.inputs import playercontroler as 							plc


class GameScreen(screen.Screen):
	def __init__(self, networkInfo):
		super().__init__()
		# Pre init the game

		# Init variable
		self.inPause = False
		self.mapChange = False
		self.networkInfo = networkInfo

		self.controlPlay1 = plc.PlayerController()
		self.controlPlay2 = plc.PlayerController()

		# Set gameHud
		self.multiPlayer = text.Text("pixel1")
		self.multiPlayer.setSize(0.4)
		self.multiPlayer.setColor([0.4,0.1,0.8,1])
		self.multiPlayer.setPosition([17.9, 0])
		self.multiPlayer.setCentering("down-right")
		self.multiPlayer.setText("")

		# Set pauseHud
		self.textPause = text.Text("pixel1")
		self.textPause.setAll("Pause", 1, [9, 11], [0.9, 0.9, 0.9, 0.9], "up")

		self.backPause = guirenderer.GuiRenderer()
		self.backPause.setImage([18, 12], "transition")
		self.backPause.setOpacity(0.3)
		self.backPause.updateModel([9, 6])

		self.bodyPause = guirenderer.GuiRenderer()
		self.bodyPause.setImage([6, 9.2], "transition")
		self.bodyPause.setOpacity(0.5)
		self.bodyPause.updateModel([9, 7])

		def funct1():
			from game.screen.gamemanager import GameManager
			GameManager.currentScreen.inPause = False

		self.pauseResume = button.Button([9, 6], [3, 1], "Reprendre", funct1)

		def funct2():
			self.setScreen("menuscreen", [True])

		self.pauseQuit = button.Button([9, 4], [3, 1], "Quitter", funct2)
	
	# Second Init, inits managers for the game after that gamescreen finish its init
	# because managers can't change a gamescreen value (inPause) during its __init__
	def init(self):
		em.init()

		player1 = pl.Player(["Player", em.PLAYER_1, [0, 0], 0, "players/player1.png"])
		em.addWithId(player1)
		player2 = pl.Player(["Player", em.PLAYER_2, [0, 0], 1, "players/player2.png"])
		em.addWithId(player2)

		mam.init()
		Hud.init()

		# Attributes an entity to controllers
		self.controlPlay1.setPlayer(em.PLAYER_1)
		self.controlPlay1.setEntity(em.entities[em.PLAYER_1])

		self.controlPlay2.setPlayer(em.PLAYER_2)
		self.controlPlay2.setEntity(em.entities[em.PLAYER_2])

		# Init network and client if game's parameter networkInfo[0] is True
		if self.networkInfo[0]:
			from game.util import client
			import time
			
			self.serverPause = True
			self.isPlayer = -1
			
			self.client = client.Client(self.networkInfo[1], int(self.networkInfo[2]))
			self.client.start()
			
			# Wait a bit for the connection
			time.sleep(self.client.timeout + 0.2)
			if self.client.connectState():
				self.client.send({0 : 0})
				self.client.receive()
			# If the connection failed, return to the menu with message screen
			else:
				self.networkInfo[0] = False
				self.client.end()
				self.inPause = True
				self.serverPause = True

				from game.screen.gamemanager import GameManager
				GameManager.setCurrentScreen("messagescreen", ["Erreur", "Connexion refusée"])

		gm.cam.trackEntity(em.PLAYER_1)

	def update(self):
		# Keys test
		if im.inputPressed(im.ESCAPE):
			self.inPause = not self.inPause

		if self.networkInfo[0]:
			self.updateMulti()
		else:
			self.updateLocal()

	# Game isn't in pause when the player press escape but only when the server decide it
	def updateMulti(self):
		if self.serverPause:
			if self.isPlayer == -1:
				self.client.send({0 : 1})
			else:
				self.client.send({0 : 2})
		else:
			if not self.mapChange:
				# Update
				self.controlPlay1.update()
				self.controlPlay2.update()

				if self.inPause:
					self.pauseResume.update()
					self.pauseQuit.update()
				else:
					if self.isPlayer == 0:
						if not self.controlPlay1.tempInputState == self.controlPlay1.inputState:
							self.client.send({1: {0: self.controlPlay1.inputState}})
					else:
						if not self.controlPlay2.tempInputState == self.controlPlay2.inputState:
							self.client.send({1: {0: self.controlPlay2.inputState}})

				em.update()

				if self.controlPlay1.inputState[0] >= 2 and self.controlPlay2.inputState[0] >= 2:
					mam.reserveChange(mam.zone, mam.id, mam.defaultEntry)

				if kbm.keyPressed(290):
					from game.game.command import Command
					Command.command(input('\n[COMMAND] $ '))

				# Dispose components
				gm.cam.goToEntity()
				em.dispose()
				Hud.dispose()

			mam.update()

		self.analyseData(self.client.data)

	# Game is in pause when the player press escape
	def updateLocal(self):
		if self.inPause:
			self.pauseResume.update()
			self.pauseQuit.update()
		elif self.mapChange:
			mam.update()
		else:
			# Update
			self.controlPlay1.update()
			self.controlPlay2.update()
			em.update()

			if self.controlPlay1.inputState[0] >= 2:
				mam.reserveChange(mam.zone, mam.id, mam.defaultEntry)

			if kbm.keyPressed(291):
				gm.cam.trackEntity(1 - gm.cam.entityId)

			if kbm.keyPressed(290):
				self.inPause = True
				from game.game.command import Command
				Command.command(input('\n[COMMAND] $ '))
				self.inPause = False

			# Dispose components
			gm.cam.goToEntity()

			em.dispose()
			Hud.dispose()
			mam.update()

	def display(self):
		mam.display()
		Hud.display()

		if self.inPause:
			self.backPause.display()
			self.bodyPause.display()
			self.textPause.display()
			self.pauseResume.display()
			self.pauseQuit.display()

		self.multiPlayer.display()

	# Analyse the data and decide with a protocol what do.
	# Field 0 correspond to the server state
	# Field 1 correspond to the other player key state
	# Field 2 is free for now
	# Field 3 correspond to the player attribution
	def analyseData(self, data):
		if data == "":
			return

		if '3' in data and self.isPlayer == -1:
			self.isPlayer = data['3']

			gm.cam.trackEntity(self.isPlayer)
			self.multiPlayer.setText("Player:" + str(self.isPlayer + 1))

			if self.isPlayer == 0:
				self.controlPlay1.multi = True
				self.controlPlay2.block = True
			else:
				self.controlPlay2.multi = True
				self.controlPlay1.block = True

		if '1' in data:
			string = data['1']
			if type(string) == str:
				print("this is a string")
				string = string.replace("[", "")
				string = string.replace("]", "")
				string = string.split(",")
				for i in range(len(string)):
					string[i] = int(string[i])
			if self.isPlayer == 0:
				self.controlPlay2.inputState = string
			else:
				self.controlPlay1.inputState = string

		if '0' in data:
			if data['0'] == 0:
				self.serverPause = False
			elif data['0'] == 1:
				self.serverPause = True

			# Server end the multi with a disconnection message
			elif data['0'] == 2:
				self.controlPlay2.multi = False
				self.controlPlay2.block = False
				self.controlPlay1.multi = False
				self.controlPlay1.block = False

				self.controlPlay1.inputState = [0, 0, 0, 0, 0, 0, 0, 0]
				self.controlPlay2.inputState = [0, 0, 0, 0, 0, 0, 0, 0]

				self.client.end()
				self.networkInfo[0] = False
				self.multiPlayer.setText("")

		self.client.data = ""

	def unload(self):
		mam.unload()
		Hud.unload()
		em.entities[em.PLAYER_1].unload()
		em.entities[em.PLAYER_2].unload()
		em.unload()

		self.multiPlayer.unload()
		self.textPause.unload()
		self.backPause.unload()
		self.bodyPause.unload()
		self.pauseResume.unload()
		self.pauseQuit.unload()

		if self.networkInfo[0]:
			self.client.end()
