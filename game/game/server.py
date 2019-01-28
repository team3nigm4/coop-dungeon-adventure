# Temporary class server

import time

from game.game.entitymanager import EntityManager as EM


class Server:

	@staticmethod
	def init():
		# Player one
		EM.add([0, 0])
		# Player two
		EM.add([4000, 4000])

		pass

	@staticmethod
	def update():
		from game.screen.gamemanager import GameManager
		# Receive and create data
		clientData = GameManager.clientData
		serverData = [0]

		if clientData[0] == 3:
			print(clientData[0])

		# Return data
		serverData.append(EM.entities[0].pos)
		serverData.append(EM.entities[1].pos)

		serverData[0] = time.time_ns()
		GameManager.serverData = serverData

	def close(self):
		pass
