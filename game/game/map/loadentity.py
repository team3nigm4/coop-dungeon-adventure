class LoadEntity:
	from game.game.entitymodel import pressureplate
	from game.game.entitymodel import door
	from game.game.entitymodel import slidingblock
	from game.game.entitymodel import activationblock
	from game.game.entitymodel import activationplate
	from game.game.entitymodel import toggleplate
	from game.game.entitymodel import spawn
	from game.game.entitymodel import player
	from game.game.entitymodel import bridge

	entities = {
		"Player" : player.Player,
		"SlidingBlock": slidingblock.SlidingBlock,
		"Door": door.Door,
		"PressurePlate": pressureplate.PressurePlate,
		"ActivationBlock": activationblock.ActivationBlock,
		"TogglePlate": toggleplate.TogglePlate,
		"ActivationPlate": activationplate.ActivationPlate,
		"Spawn" : spawn.Spawn,
		"Bridge": bridge.Bridge
	}

	@staticmethod
	def instance(args):
		if (args[0] in LoadEntity.entities):
			return LoadEntity.entities[args[0]](args)
		else: 
			return False