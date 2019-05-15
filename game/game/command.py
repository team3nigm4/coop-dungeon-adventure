# Class to apply command to control the game


class Command:

	@staticmethod
	def command(command):
		try:
			args = command.split(" ")
			getattr(Command, args[0])(args)
		except Exception as e:
			print("\n[COMMAND] Error on command " + command + "()")
			print(e)

	@staticmethod
	# 1 = functionName
	def help(args="none"):
		commandsHelp = {
			"changeMap": "Usage: changeMap [zoneName] [mapId] [entryPoint]\n  Go to a new map (alias of cm)",
			"cm": "Usage: cm [zoneName] [mapId] [entryPoint]\n  Go to a new map (alias of ChangeMap)",
			"damage": "Usage: damage [entityId] [damagesAmount]\n  Apply some damages to an entity",
			"emStatus": "  Display the current status of the entity manager",
			"help": "Usage: help {functionName}\n  Shows how to use a function\n  No argument: displays the list of available functions",
			"reloadHud": "  Reload hud informations and rebuilt it.",
			"setLife": "Usage: setLife [entityId] [lifeAmount]\n  Define the amount of life of an entity",
			"toggleBoxes": "  Toggle the display of collision boxes",
			"tpE": "Usage: tpE [entityIdToMove] [destinationEntityId]\n  Move an entity to another"
		}
		if not args == "none":
			if args[1] in commandsHelp:
				print("\n:::: Help for command " + args[1] + "() ::::")
				print(commandsHelp[args[1]] + "\n")
			else:
				print("[COMMAND] Error : No command called \"" + args[1] + "()\"")
		else:
			print("\n:::: Commands list ::::")
			for key, value in commandsHelp.items():
				print(key + "\n" + commandsHelp[key] + "\n")

	@staticmethod
	# 1 = zoneName
	# 2 = mapId
	# 3 = entryPoint
	def changeMap(args):
		from game.game.map.mapmanager import MapManager as mam
		mam.reserveChange(args[1], args[2], int(args[3]))

	@staticmethod
	# Alias of changeMap()
	def cm(args): Command.changeMap(args)

	@staticmethod
	# 1 = entityId
	# 2 = damagesAmount
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
	def reloadHud(args):
		from game.game.gameplay.hud import Hud
		Hud.unload()
		Hud.init()

	@staticmethod
	# 1 = entityId
	# 2 = lifeAmount
	def setLife(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		try:
			em.entities[int(args[1])].setLife(int(args[2]))
		except Exception as e:
			print("\nEntity is not entity complex :", em.entities[int(args[1])].type)
			print(e)

	@staticmethod
	def toggleBoxes(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		em.displayBox^= True

	@staticmethod
	# 1 = entityIdToMove
	# 2 = destinationEntityId
	def tpE(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		em.entities[int(args[1])].setPos(em.entities[int(args[2])].pos)
