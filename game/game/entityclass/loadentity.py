class LoadEntity:
	from game.game.entitymodel import activationblock
	from game.game.entitymodel import activationplate
	from game.game.entitymodel import arrow
	from game.game.entitymodel import bat
	from game.game.entitymodel import bridge
	from game.game.entitymodel import door
	from game.game.entitymodel import lockeddoor
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
		"Door": door.Door,
		"LockedDoor": lockeddoor.LockedDoor,
		"Mannequin": mannequin.Mannequin,
		"Player": player.Player,
		"PressurePlate": pressureplate.PressurePlate,
		"SlidingBlock": slidingblock.SlidingBlock,
		"Spawn": spawn.Spawn,
		"Spider": spider.Spider,
		"TogglePlate": toggleplate.TogglePlate
	}

	@staticmethod
	def instance(args):
		if args[0] in LoadEntity.entities:
			return LoadEntity.entities[args[0]](args)
		else: 
			return False
