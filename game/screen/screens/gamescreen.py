# This class performs the display and the update of the client


from game.game.entitymodel import player as pl
from game.game.entityclass.entitymanager import EntityManager as em
from game.game.map.mapmanager import MapManager as mam
from game.inputs.inputmanager import InputManager as im
from game.inputs.keyboardmanager import KeyBoardManager as kbm
from game.screen.gamemanager import GameManager as gm
from game.screen.screens import screen
from game.game.gameplay.hud import Hud
from game.render.text import text

from game.inputs import playercontroler as plc

from game.util.logger import Logger

class GameScreen(screen.Screen):

	def __init__(self, networkInfo):
		# Pre init the game
		super().__init__()

		self.inPause = False
		self.mapChange = False
		self.networkInfo = networkInfo

		self.controlPlay1 = plc.PlayerController()
		self.controlPlay2 = plc.PlayerController()

		self.text = text.Text("pixel1")
		self.text.setSize(0.4)
		self.text.setColor([0.4,0.1,0.8,1])
		self.text.setPosition([17.9, 0])
		self.text.setCentering("down-right")

	def init(self):
		# init the game
		em.init()

		player1 = pl.Player(["Player", em.PLAYER_1, [0, 0], 0, "players/player1.png"])
		em.addWithId(player1)
		player2 = pl.Player(["Player", em.PLAYER_2, [0, 0], 1, "players/player2.png"])
		em.addWithId(player2)

		mam.init()
		Hud.init()

		self.controlPlay1.setPlayer(em.PLAYER_1)
		self.controlPlay1.setEntity(em.entities[em.PLAYER_1])

		self.controlPlay2.setPlayer(em.PLAYER_2)
		self.controlPlay2.setEntity(em.entities[em.PLAYER_2])

		self.text.setText("CDA v.0.1 - network:" + str(self.networkInfo[0]))

		# init network if game in multi player
		if self.networkInfo[0]:
			from game.util import client
			import time
			
			self.client = client.Client(self.networkInfo[1], int(self.networkInfo[2]))
			self.serverPause = True
			self.isPlayer = -1
			self.client.start()

			time.sleep(self.client.timeout + 0.1)
			if self.client.connectState():
				self.client.send({0 : 0})
				self.client.receive()
			else:
				self.networkInfo[0] = False
				self.client.end()

		if not self.networkInfo[0]:
			self.inPause = False
			self.serverPause = False
			gm.cam.trackEntity(em.PLAYER_1)

		self.text.setText("CDA v.0.1 - network:" + str(self.networkInfo[0]))

	def update(self):
		# Keys test
		if im.inputPressed(im.ESCAPE):
			from game.screen import  gamemanager
			gamemanager.GameManager.setCurrentScreen("MenuScreen", [True])

		if self.networkInfo[0]:
			self.updateMulti()
		else:
			self.updateLocal()

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

				if self.isPlayer == 0:
					if not self.controlPlay1.tempInputState == self.controlPlay1.inputState:
						self.client.send({1 : { 0 : self.controlPlay1.inputState}})
				else:
					if not self.controlPlay2.tempInputState == self.controlPlay2.inputState:
						self.client.send({1 : { 0 : self.controlPlay2.inputState}})

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

	def updateLocal(self):
		if not self.inPause and not self.mapChange:
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

		else:
			pass

		mam.update()

	def display(self):
		mam.display()
		Hud.display()
		self.text.display()

	def unload(self):
		mam.unload()
		Hud.unload()
		em.entities[em.PLAYER_1].unload()
		em.entities[em.PLAYER_2].unload()
		em.unload()
		self.text.unload()

		if self.networkInfo[0]:
			self.client.end()

	def analyseData(self, data):
		if data == "":
			return

		print(data)
		if '3' in data and self.isPlayer == -1:
			self.isPlayer = data['3']

			gm.cam.trackEntity(self.isPlayer)
			self.text.setText(self.text.text + "\n Player:" + str(self.isPlayer + 1))

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
			elif data['0'] == 2:
				self.controlPlay2.multi = False
				self.controlPlay2.block = False
				self.controlPlay1.multi = False
				self.controlPlay1.block = False

				self.controlPlay1.inputState = [0, 0, 0, 0, 0, 0, 0, 0]
				self.controlPlay2.inputState = [0, 0, 0, 0, 0, 0, 0, 0]

				self.client.end()
				self.networkInfo[0] = False
				self.text.setText("CDA v.0.1 - network:" + str(self.networkInfo[0]))

		self.client.data = ""
