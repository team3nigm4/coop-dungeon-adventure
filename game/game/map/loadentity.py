class LoadEntity:
	from game.game.entitymodel import pressureplate
	from game.game.entitymodel import door
	from game.game.entitymodel import slidingblock
	from game.game.entitymodel import activationblock
	from game.game.entitymodel import activationplate

	entities = {
		"SlidingBlock": slidingblock.SlidingBlock,
		"Door": door.Door,
		"PressurePlate": pressureplate.PressurePlate,
		"ActivationBlock": activationblock.ActivationBlock,
		"ActivationPlate": activationplate.ActivationPlate
	}

	@staticmethod
	def instance(args):
		return LoadEntity.entities[args[0]](args)