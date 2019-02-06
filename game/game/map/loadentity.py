class LoadEntity:
	from game.game.entitymodel import pressureplate
	from game.game.entitymodel import door
	from game.game.entitymodel import slidingblock
	from game.game.entitymodel import activationblock
	from game.game.entitymodel import activationplate
	from game.game.entitymodel import toggleplate

	entities = {
		"SlidingBlock": slidingblock.SlidingBlock,
		"Door": door.Door,
		"PressurePlate": pressureplate.PressurePlate,
		"ActivationBlock": activationblock.ActivationBlock,
		"TogglePlate": toggleplate.TogglePlate,
		"ActivationPlate": activationplate.ActivationPlate
	}

	@staticmethod
	def instance(args):
		return LoadEntity.entities[args[0]](args)