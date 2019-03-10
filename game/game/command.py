class Command:

	@staticmethod
	def command(command):
		try:
			args = command.split(" ")
			getattr(Command, args[0])(args)
		except Exception as e:
			print("\nError on command :" + command)
			print(e)

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

	@staticmethod
	# 1 = entity
	# 2 = damage
	def damage(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		try:
			em.entities[int(args[1])].setLife(em.entities[int(args[1])].life - int(args[2]))
		except:
			print("\nEntity is not entity complex :", em.entities[int(args[1])].type)

	@staticmethod
	def emStatus(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		em.status()

	@staticmethod
	def help(args):
		print("\n:::Help:::\n\n"
			  "cm/ChangeMap: Go to a new map.\n Args: zone (test), mapID (map1) and entryPoint (0).\n\n"
			  "damage: Apply some damages to an entity.\n Args: entityId (0) and damage(s) (0).\n\n"
			  "emStatus: Know the current status of the entity manager.\n No Argument.\n\n"
			  "help: Get informations about functions.\n No Argument.\n\n"
			  "rechargeHud: Recharge the hud info and rebuilt the hud.\n\n"
			  "setLife: Set the life of an entity.\n Args: entityId (0) and new life (0).\n\n"
			  "toggleBox: Toggle the display of collision boxes."
			  "tpE: Move one entity to another.\n Args: entityID to tansport (0) and arrival entityID (1).")

	@staticmethod
	# 1 = entity
	# 2 = newLife
	def rechargeHud(args):
		from game.game.gameplay.hud import Hud
		Hud.unload()
		Hud.init()

	@staticmethod
	# 1 = entity
	# 2 = newLife
	def setLife(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		try:

			em.entities[int(args[1])].setLife(int(args[2]))
		except Exception as e:
			print("\nEntity is not entity complex :", em.entities[int(args[1])].type)
			print(e)

	@staticmethod
	def toggleBox(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		if em.displayBox == True:
			em.displayBox = False
		else:
			em.displayBox = True

	@staticmethod
	# 1 = entity1
	# 2 = entity2
	def tpE(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		em.entities[int(args[1])].setPos(em.entities[int(args[2])].pos)

