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

from game.util import client


class GameScreen(screen.Screen):

	def __init__(self, networkInfo):
		# Pre init the game
		super().__init__()

		self.inPause = False
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
			self.client = client.Client(self.networkInfo[1], str(self.networkInfo[2]))
			self.serverPause = True
			self.client.connection()

			if self.client.connectState():
				self.client.send("connection")
				self.client.receive()
			else:
				self.networkInfo[0] = False

		if not self.networkInfo[0]:
			self.inPause = False
			self.serverPause = False
			gm.cam.trackEntity(em.PLAYER_1)

		self.text.setText("CDA v.0.1 - network:" + str(self.networkInfo[0]))

	def update(self):

		# Keys test
		if im.inputPressed(im.ESCAPE):
			from game.main.window import Window
			Window.exit()

		if self.serverPause and self.networkInfo[0]:
			self.send("wait")

		if self.networkInfo[0]:
			self.receive()

		if True:
			# Update
			self.controlPlay1.update()
			self.controlPlay2.update()
			em.update()

			if im.inputPressed(im.RESET):
				mam.reserveChange(mam.zone, mam.id, mam.defaultEntry)

			if im.inputPressed(im.ITEM2_0):
				gm.cam.trackEntity(1 - gm.cam.entityId)

			if kbm.getKey(290):
				from game.game.command import Command
				Command.command(input('\n[COMMAND] $ '))

			# Dispose components
			gm.cam.goToEntity()
			em.dispose()
			Hud.dispose()

			mam.update()
		else:
			pass

	def display(self):
		mam.display()
		Hud.display()
		self.text.display()

	def unload(self):
		if self.networkInfo[0]:
			self.conn.close()
		mam.unload()
		Hud.unload()
		em.entities[em.PLAYER_1].unload()
		em.entities[em.PLAYER_2].unload()
		self.text.unload()

	def analyseData(self):
		print(self.data)
		if self.me in self.data:
			if "player" in self.data[self.me]:
				self.player = self.data[self.me]["player"]
				gm.cam.trackEntity(self.player - 1)
				print()
				self.text.setText(self.text.text + "\n Player:" + str(self.player))

		if "all" in self.data:
			if self.data["all"] == "play":
				print("game started")
				self.serverPause = False
			elif self.data["all"] == "stop":
				self.serverPause = True
