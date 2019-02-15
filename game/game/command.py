

class Command:

	@staticmethod
	def command(command):
		try:
			args = command.split(" ")
			getattr(Command, args[0])(args)
		except Exception as e:
			print("\nError on command :" +  command)
			print(e)


	@staticmethod
	# 1 = entity
	# 2 = damage
	def damage(args):
		try :
			from game.game.entityclass.entitymanager import EntityManager as em
			em.entities[int(args[1])].setLife(em.entities[int(args[1])].life - int(args[2]))
		except:
			print("\nEntity is not entity complexe :", em.entities[int(args[1])].type)

	@staticmethod
	def emStatus(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		em.status()

	@staticmethod
	# 1 = entity
	# 2 = newLife
	def setLife(args):
		try :
			from game.game.entityclass.entitymanager import EntityManager as em
			em.entities[int(args[1])].setLife(int(args[2]))
		except Exception as e:
			print("\nEntity is not entity complexe :", em.entities[int(args[1])].type)
			print(e)

	@staticmethod
	# 1 = entity1
	# 2 = entity2
	def tpE(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		em.entities[int(args[1])].setPos(em.entities[int(args[2])].pos)

	@staticmethod
	# 1 = zone
	# 2 = map name
	# 3 = entry point
	def changeMap(args):
		from game.game.map.mapmanager import MapManager as mam
		mam.reserveChange([args[1], args[2], int(args[3])])

	@staticmethod
	def cm(args):
		Command.changeMap(args)