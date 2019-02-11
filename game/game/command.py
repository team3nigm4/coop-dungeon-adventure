

class Command:

	@staticmethod
	def command(command):
		try:
			args = command.split(" ")
			getattr(Command, args[0])(args)
		except :
			print("\nError on command :" +  command)

	@staticmethod
	# 1 = entity1
	# 2 = entity2
	def tpE(args):
		from game.game.entityclass.entitymanager import EntityManager as em
		print("tpE", args)
		em.entities[int(args[1])].setPos(em.entities[int(args[2])].pos)

