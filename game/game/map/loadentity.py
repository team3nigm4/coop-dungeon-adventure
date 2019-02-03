class LoadEntity:
	from game.game.entitymodel import pressureplate
	from game.game.entitymodel import door
	from game.game.entitymodel import slidingblock

	entities = {
		"SlidingBlock": slidingblock.SlidingBlock,
		"Door": door.Door,
		"PressurePlate": pressureplate.PressurePlate
	}

	@staticmethod
	def instance(args):
		return LoadEntity.entities[args[0]](args)