# Class to load entity from args

class LoadEntity:
	from game.game.entitymodel import activationblock
	from game.game.entitymodel import activationplate
	from game.game.entitymodel import arrow
	from game.game.entitymodel import bat
	from game.game.entitymodel import bridge
	from game.game.entitymodel import decor
	from game.game.entitymodel import tp
	from game.game.entitymodel import  interactionswitch
	from game.game.entitymodel import itemrecoverable
	from game.game.entitymodel import padlock
	from game.game.entitymodel import mannequin
	from game.game.entitymodel import player
	from game.game.entitymodel import pressureplate
	from game.game.entitymodel import slidingblock
	from game.game.entitymodel import spawn
	from game.game.entitymodel import spider
	from game.game.entitymodel import toggleplate

	entities = {
		"ActivationBlock": activationblock.ActivationBlock,
		"ActivationPlate": activationplate.ActivationPlate,
		"Arrow": arrow.Arrow,
		"Bat": bat.Bat,
		"Bridge": bridge.Bridge,
		"Decor": decor.Decor,
		"Tp": tp.Tp,
		"InteractionSwitch" : interactionswitch.InteractionSwitch,
		"ItemRecoverable": itemrecoverable.ItemRecoverable,
		"Padlock": padlock.Padlock,
		"Mannequin": mannequin.Mannequin,
		"Player": player.Player,
		"PressurePlate": pressureplate.PressurePlate,
		"SlidingBlock": slidingblock.SlidingBlock,
		"Spawn": spawn.Spawn,
		"Spider": spider.Spider,
		"TogglePlate": toggleplate.TogglePlate
	}

	# Entities that should not be instantiated
	noError = [
		"SpawnPoint"
	]

	# Some entity that should not be instantiated during a reset of a map
	# reset = 0, no reset = 1
	LIST_RESET = {
		"ActivationBlock": 0,
		"ActivationPlate": 0,
		"Arrow": 0,
		"Bat": 0,
		"Bridge": 0,
		"Decor": 0,
		"Tp": 0,
		"InteractionSwitch": 0,
		"ItemRecoverable": 1,
		"Padlock": 1,
		"Mannequin": 0,
		"Player": 1,
		"PressurePlate": 0,
		"SlidingBlock": 0,
		"Spawn": 0,
		"Spider": 0,
		"TogglePlate": 0
	}

	TO_RESET = 0
	NO_RESET = 1

	# This attribute will be change during a reset of a map
	reset = False

	@staticmethod
	def setReset(state):
		LoadEntity.reset = state

	@staticmethod
	def instance(args):
		# If the instance complete without problem
		try:
			if args[0] in LoadEntity.entities:
				if LoadEntity.reset:
					if not LoadEntity.isResetable(args):
						return ["False", "No Error"]
					else:
						return ["True", LoadEntity.entities[args[0]](args)]
				else:
					return ["True", LoadEntity.entities[args[0]](args)]
			else:
				if args[0] in LoadEntity.noError:
					return ["False", "No Error"]
				else:
					return ["False", "This type of entity doesn't exist"]
		except Exception as e:
			return ["False", e]

	@staticmethod
	def isResetable(arg):
		type = arg[0]
		count = 0
		# Spawn can be reset, but spawn can contain an un resetable entity.
		# Loop to test is the spawn contains this type ogf entity.
		if type == "Spawn":
			arg = arg[LoadEntity.entities["Spawn"].ARGS_ENTITY_INFO]
			while type == "Spawn":
				temp = arg
				for i in range(count):
					temp = temp[3]

				if not temp[0] == "Spawn":
					type = temp[0]
				else:
					count +=1

		return LoadEntity.LIST_RESET[type] == LoadEntity.TO_RESET
